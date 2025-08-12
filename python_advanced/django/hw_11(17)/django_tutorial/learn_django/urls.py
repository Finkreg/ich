"""
URL configuration for learn_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from library.views import book_list_create, book_detail_update_delete
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')), # fro example if we are going to localhost:8000/blog/about, this path cuts off 
    # blog/ part and sends to blog.urls only about/ part looking for a match
    path('project/', include('project.urls')),
    path('task_manager/', include('task_manager.urls',)),
    path('books/', book_list_create, name='book-list-create'),  # Для получения всех книг и создания новой книги
    path('shop/', include('shop.urls')),
    path('books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'),  # Для операций с одной книгой
]
