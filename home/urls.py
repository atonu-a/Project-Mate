from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('feed', views.discover, name="discover"),
    path('get-started/', views.landing_page, name="overview"),
    path('search/', views.search_results, name="search_results"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('messages/', views.messages, name="messages"),
    path('notifications/', views.notifications, name="notifications"),
    
    
]
