"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # API Endpoints
    path('api/signup/', views.signup, name='signup'),  # This is for the signup API (POST request)
    path('api/login/', views.login, name='login'),

    # URL for Signin and Signup Pages (GET requests)
    path('signin/', views.signin_page, name='signin_page'),  # This is for rendering the signin form (GET request)
    path('signup/', views.signup_page, name='signup_page'),  # This is for rendering the signup form (GET request)

    path('api/hospitals/', views.get_hospitals, name='get_hospitals'),
    path('api/add_hospital/', views.add_hospital, name='add_hospital'),

    path('hospitals/', views.hospitals, name='hospitals'),
    path('list_hospitals/', views.list_hospitals_page, name='list_hospitals_page'),

    path('api/cities/', views.get_cities, name='get_cities'),
    path('api/hospitals/', views.hospitals, name='hospitals'),

    path('search/', views.search_hospitals, name='search_hospitals'),
]

