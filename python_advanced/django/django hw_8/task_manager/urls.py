from django.urls import path
from task_manager.views import *
from . import views

urlpatterns = [
    path('tasks/', views.task_list_create, name='task_list_create'),
    path('tasks/<int:pk>/', views.get_task_details, name='get-task-details'),
    path('tasks/stats/', views.task_stats, name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),
    path('tasks/by-day/',TaskListByDay.as_view(), name='tasks-by-day')
]