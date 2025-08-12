from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskListCreateView, TaskDetailView,
    SubTaskListCreateView, SubTaskDetailView,
    FilteredSubTaskListView, TaskListByDay,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-detail'),

    path('subtasks/filter/', FilteredSubTaskListView.as_view(), name='subtask-filtered'),
    path('tasks/by-day/', TaskListByDay.as_view(), name='task-by-day'),

    path('', include(router.urls)),  # 🔥 ВАЖНО: подключение маршрутов от роутера
]
