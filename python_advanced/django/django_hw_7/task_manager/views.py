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
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data)
    
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
    