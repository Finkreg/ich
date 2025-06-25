from project.views import test
from django.urls import path, include
urlpatterns = [
    path('test', view=test)
]