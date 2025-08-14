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
# from django.contrib import admin
# from django.urls import path, include
# from library.views import book_list_create, book_detail_update_delete
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('blog/', include('blog.urls')), # fro example if we are going to localhost:8000/blog/about, this path cuts off 
#     # blog/ part and sends to blog.urls only about/ part looking for a match
#     path('project/', include('project.urls')),
#     path('task_manager/', include('task_manager.urls',)),
#     path('books/', book_list_create, name='book-list-create'),  # Для получения всех книг и создания новой книги
#     path('shop/', include('shop.urls')),
#     path('books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'),  # Для операций с одной книгой
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
# ]
from django.contrib import admin
from django.urls import path, include
from library.views import book_list_create, book_detail_update_delete
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Task Manager API",
      default_version='v1',
      description="API documentation for Task Manager",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('project/', include('project.urls')),
    path('task_manager/', include('task_manager.urls')),
    path('books/', book_list_create, name='book-list-create'),
    path('shop/', include('shop.urls')),
    path('books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
