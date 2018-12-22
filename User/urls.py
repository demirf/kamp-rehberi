from django.contrib import admin
from django.urls import path
from . import views

app_name = 'User'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.loginUser, name = 'login'),
    path('logoutUser/', views.logoutUser, name = 'logout'),
    
]
