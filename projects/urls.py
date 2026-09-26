from django.contrib import admin
from django.urls import path
from projects import views

urlpatterns = [
    path('<str:slug>/', views.project_detail, name='project_detail'),
]


