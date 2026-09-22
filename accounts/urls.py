from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('signin/', views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path('signup/', views.signup, name="signup"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('complete-profile/', views.complete_profile, name="complete_profile"),
]
