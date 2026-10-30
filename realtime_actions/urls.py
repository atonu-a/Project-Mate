from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [   
    path('notifications/', views.notification_view, name="notifications"),
    path('<int:pk>/read', views.read_notice, name="read_notice"),

]