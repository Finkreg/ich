from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone

from .models import Listing, Review, SearchHistory, Booking
from .serializers import ListingSerializer, ListingDetailSerializer, ReviewSerializer, BookingSerializer
from users.permissions import IsLandlord, IsOwnerOrReadOnly
from .filters import ListingFilter
# Create your views here.


class ListingViewSet(viewsets.ModelViewSet):
    """Viewset to operate the ads (CRUD)"""
    #queryset = Listing.objects.filter(is_active=True) #by default we show only active listings

    #redefined queryset so the owner can have access and "ressurrect" inactive listing
    # def get_queryset(self):
    #     if self.action == 'toggle_active':
    #         return Listing.objects.all()
    #     return Listing.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ListingFilter

    ordering_fields = [
        'price_per_night',
        'created_at',
        'views_count',
        'num_reviews'
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        base_queryset = Listing.objects.all() if self.action == 'toggle_active' else Listing.objects.filter(is_active=True)
        return base_queryset.annotate(
            num_reviews=models.Count('reviews', distinct=True)
        )


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ListingDetailSerializer #for detailed view
        return ListingSerializer
    
    def get_permissions(self):
        """Lets set permissions for different operations"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'toggle_active']:
            #only Landlords can create, update and change status and only of the listing that belong them
            self.permission_classes = [IsAuthenticated, IsLandlord, IsOwnerOrReadOnly]
        elif self.action == 'retrieve':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.AllowAny]
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



    #Custom endpoint inside ViewSet (/listings/<id>/toggle_active/) Only method 'PATCH' is allowed
    # and only for Landlords. 
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsLandlord, IsOwnerOrReadOnly])
    def toggle_active(self, request, pk=None):
        listing = self.get_object()
        listing.is_active = not listing.is_active #turns True if was False and viceversa
        listing.save()
        serializer = self.get_serializer(listing)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def increment_views(self, request, pk=None):
        """
        Function to increase the view counter.
        """
        listing = self.get_object()
        listing.views_count += 1
        listing.save()
        return Response({'views_count': listing.views_count}, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def popular_listings(self, request):
        """Returns the list sorted by views count (most popular)"""
        popular_listings = self.get_queryset().order_by('-views_count')[:10] # Топ-10
        serializer = self.get_serializer(popular_listings, many=True)
        return Response(serializer.data)
    
    
    def list(self, request, *args, **kwargs):
        """custom method to save search history"""
        response = super().list(request, *args, **kwargs)
        search_query = request.query_params.get('search', None)
        if search_query and request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=search_query)
        
        return response


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet to operate the reviews.
    """
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        # Reviews are always linked to certain listing
        return Review.objects.filter(listing_id=self.kwargs['listing_pk'])

    def get_permissions(self):
        """
        Sets permissions to operate the reviews
        """
        if self.action == 'create':
            # Only authenticated users can create reviews
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # only author can update/delete reviews
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyReview] # Need to create IsOwnerOrReadOnlyReview
        else: # list, retrieve
            # Everyone can view the reviews
            self.permission_classes = [permissions.AllowAny]
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
        # We're linking the review to  actual user and listing
        listing = get_object_or_404(Listing, pk=self.kwargs['listing_pk'])
        user = self.request.user

        #checking if user has the approved booking
        has_completed_booking = Booking.objects.filter(
            listing=listing,
            tenant=user,
            status='confirmed',
            end_date__lt=timezone.now().date()
        ).exitst()

        if not has_completed_booking:
            raise serializers.ValidationError(
                {"detail": "You can leave review only after the the booking period has ended"}
            )
        #lets save the review if the verification has passed
        serializer.save(reviewer=user, listing=listing)

# Additional permission for reviews
class IsOwnerOrReadOnlyReview(permissions.BasePermission):
    """
    Custom permission for reviews: owner can create/edit/delete, others only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user
    

class IsBookingTenant(permissions.BasePermission):
    """Custom permission that allows access to booking only for tenants"""
    message = 'you are not the tenant of this booking'

    def has_object_permission(self, request, view, obj):
        return obj.tenant == request.user


class BookingViewSet(viewsets.ModelViewSet):
    """Viewset to operate the bookings"""
    serializer_class = BookingSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'listing', 'start_date', 'end_date']
    ordering_fields = ['created_at', 'start_date', 'status']

    def get_queryset(self):
        """Landlords see all the bookings for their ads
        Tenants see only their bookings"""
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all()
        
        if user.groups.filter(name='Landlords').exists():
            return Booking.objects.filter(listing__owner=user)
        

        return Booking.objects.filter(tenant=user)
    

    def get_permissions(self):
        """
        Set permissions to operate the bookings
        """
        # Any authenticated user may create bookings
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        # View (list, details) - as defined in get_queryset()
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated] #Only authenticated users
        # decline booking - only tenant
        elif self.action == 'cancel':
            self.permission_classes = [permissions.IsAuthenticated, IsBookingTenant]
        # Approve/decline of booking allowed only for Landlord
        elif self.action in ['confirm', 'reject']:
            self.permission_classes = [permissions.IsAuthenticated, IsLandlord] # need new permission IsOwnerOfBookingListing
        # Update/delete (if allowed) - only tenant and Landlord
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser] # only admin can update/delete
        else:
            self.permission_classes = [permissions.IsAuthenticated] # По умолчанию для других действий
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        Landlord is assigned automatically.
        """
        # Make sure landlord cannot book his own listing
        listing = serializer.validated_data['listing']
        if listing.owner == self.request.user:
            raise serializers.ValidationError("You cannot book your own listing.")
            
        serializer.save(tenant=self.request.user, status='pending') # default status 'pending'

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsBookingTenant])
    def cancel(self, request, pk=None):
        """
        Landlord can decline booking by specific date.
        """
        booking = self.get_object()
        
        # checking that booking is not yet confirmed or has ended
        if booking.status not in ['pending', 'confirmed']:
            return Response({"detail": "Booking cannot be declined."}, status=status.HTTP_400_BAD_REQUEST)
        

        booking.status = 'cancelled'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsLandlord]) #IsOwnerOfBookingListing
    def confirm(self, request, pk=None):
        """
        Landlord can approve booking request.
        """
        booking = self.get_object()
        
        if booking.status != 'pending':
            return Response({"detail": "Booking is not currently in 'Pending' status."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check that booking is not overlapping with other bookings
        overlapping_bookings = Booking.objects.filter(
            listing=booking.listing,
            status='confirmed',
            start_date__lt=booking.end_date,
            end_date__gt=booking.start_date
        ).exclude(pk=booking.pk) # exclude actual booking
        
        if overlapping_bookings.exists():
            return Response({"detail": "This Booking overlaps existing booking."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'confirmed'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsLandlord, ]) #IsOwnerOfBookingListing
    def reject(self, request, pk=None):
        """
        Landlord can decline booking request.
        """
        booking = self.get_object()
        
        if booking.status != 'pending':
            return Response({"detail": "Booking is not in 'Pending' status and cannot be declined."}, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'rejected'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IsOwnerOfBookingListing(permissions.BasePermission):
    """
    Permission that allows access if user is Landlord and posesses the listing linked to the booking.
    """
    message = 'You are not the listing owner.'

    def has_object_permission(self, request, view, obj):
        return obj.listing.owner == request.user