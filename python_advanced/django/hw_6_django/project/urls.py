from project.views import test, list_projects
from django.urls import path, include
urlpatterns = [
    #path('test', view=test),
    path('test', view=test),
    #path('project_admin', view=test),
    path('projects', view=list_projects),

]