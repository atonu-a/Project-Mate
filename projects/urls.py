from django.contrib import admin
from django.urls import path
from projects import views

urlpatterns = [
    path('create/', views.create_project, name="create"),
    path('my-projects/', views.my_projects, name="my_projects"),
    path('<str:slug>/edit', views.edit_project, name="edit_project"),
    path('<str:slug>/', views.project_detail, name='project_detail'),
    
]
