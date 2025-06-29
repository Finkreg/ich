from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list_create, name='task_list_create'),
    path('tasks/<int:pk>/', views.get_task_details, name='get-task-details'),
    path('tasks/stats/', views.task_stats, name='task-stats'),
]