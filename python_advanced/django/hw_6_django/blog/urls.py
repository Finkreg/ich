from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'), # if this receives from jango urls.py the about/ adress
    # it processes it  with views.about function.
]