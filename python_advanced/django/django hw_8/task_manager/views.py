from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTask
from .serializers import *
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils.timezone import now
from rest_framework.views import APIView
from django.db.models.functions import ExtractDay
from .paginator import SubTaskPagination
# Create your views here.

@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method =='GET':
        tasks = Task.objects.all()
        serializer = TaskModelSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_task_details(request, pk):
    task = get_object_or_404(Task, pk=pk)
    serializer = TaskModelSerializer(task)
    return Response(serializer.data)

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


class SubTaskListCreateView(APIView):

    def get(self, request, *args, **kwargs):
        subtasks = SubTask.objects.all().order_by('-created_at')
        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = SubTaskCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubTaskDetailUpdateDeleteView(APIView):

    def get_object(self, pk):
        return get_object_or_404(SubTask, pk=pk)
    
    def get(self, request, pk, *args, **kwargs):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)
    
    def put(self, request, pk, *args, **kwargs):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class TaskListByDay(APIView):

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
        
        