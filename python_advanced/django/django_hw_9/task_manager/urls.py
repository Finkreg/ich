from django.urls import path
from task_manager.views import *
from . import views
from .views import (
    TaskListCreateView, TaskDetailView,
    SubTaskListCreateView, SubTaskDetailView,
    FilteredSubTaskListView, TaskListByDay
)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-detail'),

    path('subtasks/filter/', FilteredSubTaskListView.as_view(), name='subtask-filtered'),
    path('tasks/by-day/', TaskListByDay.as_view(), name='task-by-day'),
]


# urlpatterns = [
#     path('tasks/', views.task_list_create, name='task_list_create'),
#     path('tasks/<int:pk>/', views.get_task_details, name='get-task-details'),
#     path('tasks/stats/', views.task_stats, name='task-stats'),
#     path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
#     path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),
#     path('tasks/by-day/',TaskListByDay.as_view(), name='tasks-by-day')
# ]

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-detail'),

    path('subtasks/filter/', FilteredSubTaskListView.as_view(), name='subtask-filtered'),
    path('tasks/by-day/', TaskListByDay.as_view(), name='task-by-day'),
]