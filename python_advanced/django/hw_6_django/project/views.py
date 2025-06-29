from django.shortcuts import render
from django.http import HttpResponse
from project.models import Project, Task
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .serializers import ProjectListSerializer
from rest_framework.response import Response 
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def list_projects(request):
    projects = Project.objects.all()
    if projects.exists():
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Projects not found'}, status=status.HTTP_400_BAD_REQUEST)








def test(req):
    # new_project = Project(name='Web Application', description='my_new_web_application', lang="c#")
    # new_project.save()
    # to_del = Project.objects.filter(id__gt=4)
    # to_del.delete()
    # Project.objects.create(name='Mobile Application', description='application for ios', lang="c#")
    

    # project1 = Project(name='Video enchancer', description='enchancement for video', lang="c#")
    # project2 = Project(name='Online pdf reader', description='mweb pdf application', lang="py")
    # project3 = Project(name='weather widget', description='front weather widget', lang="js")
    # projects = [project1, project2, project3]
    # Project.objects.bulk_create(projects)

    # all_objects = Project.objects.all()
    # for object in all_objects:
    #     object.lang = 'py'
    # Project.objects.bulk_update(all_objects, ['lang'])

    #Project.objects.update(name=Concat(F('name'), Value(' '), F('lang')))

    # projects = Project.objects.filter(created_at__lte="2025-06-29")
    # for project in projects:
    #     print(f"{project.name}")
    # print(f"number of projects is {projects.count()}")

    #annotate projects checking the day
    # annotated_projects = Project.objects.annotate(week_day=ExtractWeekDay("created_at"))
    # projects_per_day = annotated_projects.filter(week_day = 6)
    # for project in annotated_projects:
    #     print(project.name)

    # tasks = Task.objects.all().order_by('priority', '-due_date')
    # for task in tasks:
    #     print(f"Task title is {task.name}, has priority: {task.priority}, and deadline at: {task.due_date}")



    return HttpResponse("test")

