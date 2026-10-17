from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [   
    path("project/<str:slug>/send-join-request/", views.send_request, name="send_request"),
    path("<int:request_id>/accept/", views.accept_request, name = "accept_request"),
    path("<int:request_id>/reject/", views.reject_request, name = "reject_request"),
    path('requests/', views.join_requests, name="requests"),
    path("<str:slug>/save/", views.save_project, name="save_project"),
    path("profile/<str:username>/saved", views.saved_page, name="saved"),
    path("profile/<str:username>/follow/", views.toggle_follow, name="follow"),
    path("project/<str:slug>/like", views.like_project, name="like_project"),
]