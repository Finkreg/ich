from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.db import models


from .serializers import UserRegisterSerializer, UserLoginSerializer, SearchHistorySerializer
from listings.models import SearchHistory
# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """API View to register new users"""
    queryset = User.objects.all()
    permission_classes = (AllowAny, ) # Allow the access without authentification
    serializer_class = UserRegisterSerializer

    #redefined POST method for additional logic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Automatic login after registration and token issue
        refresh = RefreshToken.for_user(user)
        return Response({
            'user':{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """API VIEW for user's login and obtaining JWT tokens"""
    permission_classes = (AllowAny,)  # enable access without authentication
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Custom authentication: find user by email
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Wrong authentication data'}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserViewSet(viewsets.GenericViewSet):
    """Viewset linked to user actions"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search_history(self, request):
        history = SearchHistory.objects.filter(user = request.user).order_by('-searched_at')
        serializer = SearchHistorySerializer(history, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def popular_searches(self, request):
        """returns most popular search queries"""
        popular_queries = SearchHistory.objects.values('query') \
                                            .annotate(count=models.Count('query')) \
                                            .order_by('-count')[:10]
        
        return Response([item['query'] for item in popular_queries])