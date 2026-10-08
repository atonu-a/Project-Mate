from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [   
    path("<str:slug>/send-join-request/", views.send_request, name="send_request"),
    path("<int:request_id>/accept/", views.accept_request, name = "accept_request"),
    path("<int:request_id>/reject/", views.reject_request, name = "reject_request"),
    path('requests/', views.join_requests, name="requests"),
]