from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskModelSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils.timezone import now

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