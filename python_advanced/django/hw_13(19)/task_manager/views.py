from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Task, SubTask
from .serializers import *
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils.timezone import now
from rest_framework.views import APIView
from django.db.models.functions import ExtractDay
from .paginator import SubTaskPagination
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategoryCreateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwner
# Create your views here.

@api_view(['GET'])
def task_stats(request):
    total_tasks = Task.objects.count()
    status_counts = Task.objects.values('status').annotate(count=Count('id'))
    overdue_tasks = Task.objects.filter(
        Q(deadline__lt=now().date()) & ~Q(status='done')
    ).count()
    status_summary = {item['status']: item['count'] for item in status_counts}
    return Response({
        'total_tasks': total_tasks,
        'status_counts': status_summary,
        'overdue_tasks': overdue_tasks
    })

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline', 'title']  # Фильтрация
    search_fields = ['title', 'description']   # Поиск
    ordering_fields = ['created_at']           # Сортировка
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer



class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.select_related('task').all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']  # Фильтрация
    search_fields = ['title', 'description']   # Поиск
    ordering_fields = ['created_at']           # Сортировка
    ordering = ['-created_at']


class SubTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer





class TaskListByDay(APIView):
    serializer_class = TaskModelSerializer

    def get(self, request, *args, **kwargs):
        day_param = request.GET.get('day')

        if day_param:
            day_map = {
                'Monday':2,
                'Tuesday':3,
                'Wednesday':4,
                'Thursday':5,
                'Friday':6,
                'Saturday':7,
                'Sunday':1
            }
        
            weekday_num = day_map.get(day_param.capitalize())
            if weekday_num is None:
                return Response({'error': 'invalid day name'}, status=status.HTTP_400_BAD_REQUEST)
            tasks = Task.objects.annotate(day=ExtractDay('deadline')).filter(weekday=weekday_num)
        else: 
            tasks = Task.objects.all()
        
        serializer = TaskModelSerializer(tasks, many=True)
        return Response(serializer.data)

    
class FilteredSubTaskListView(APIView):
    serializer_class = SubTaskCreateSerializer

    def get(self, request, *args, **kwargs):
        task_title = request.GET.get('task_title')
        status_param = request.GET.get('status')

        # Basic queryset
        subtasks = SubTask.objects.select_related('task').order_by('-created_at')

        # implementing filtrations
        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)
        if status_param:
            subtasks = subtasks.filter(status=status_param)

        # Pagination
        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskCreateSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
        


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=['get'], serializer_class=CategoryCreateSerializer)
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        task_count = category.tasks.count()
        return Response({'category': category.name, 'task_count': task_count})
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action == 'retrieve':
            return TaskDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskCreateSerializer  # или TaskModelSerializer, если не нужно обрабатывать category
        return TaskModelSerializer

    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskModelSerializer(tasks, many=True)
        return Response(serializer.data)