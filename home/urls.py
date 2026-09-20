from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.discover, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create/', views.create, name="create"),
    path('requests/', views.requests, name="requests"),
    path('messages/', views.messages, name="messages"),
    path('notifications/', views.notifications, name="notifications"),
    path('profile/', views.profile, name="profile"),
    path('my-projects/', views.my_projects, name="my-projects"),
    path('project/<str:project_id>/', views.project_detail, name='project_detail'),
]
