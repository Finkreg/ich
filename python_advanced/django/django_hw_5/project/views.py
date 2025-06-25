from django.shortcuts import render
from django.http import HttpResponse
from project.models import Project
from django.db.models import F, Value
from django.db.models.functions import Concat

# Create your views here.
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

    Project.objects.update(name=Concat(F('name'), Value(' '), F('lang')))


    return HttpResponse("test")

    