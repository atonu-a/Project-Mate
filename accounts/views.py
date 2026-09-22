from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
# Create your views here.
# ======================
#       Registrantion
# ======================

def signup(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.first_name = user_form.cleaned_data.get('first_name')
            user.last_name = user_form.cleaned_data.get('last_name')
            user.email = user_form.cleaned_data.get('email')
            
            user.save()
            login(request, user)
            messages.success(request, "Account created and logged in successfully!")
            return redirect('complete_profile')
    
    else:
        user_form = RegistrationForm()
    
    context = {
        'user_form':user_form
    }
    
    return render(request, "signup.html", context)



# ======================
#  Profile Completeion
# ======================
def complete_profile(request):
    return render(request, "profile-setup.html")


# ======================
#       Signout
# ======================
def signout(request):
    logout(request)
    return redirect('signin')


# ======================
#       Signin
# ======================
def signin(request):
    if request.method == "POST":
        user_form = AuthenticationForm(request, data=request.POST)
        if user_form.is_valid():
            user = user_form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')
        else:
            messages.success(request, "Invalid username or password.")
       
    else:
        user_form = AuthenticationForm()
       
    context = {
        'user_form':user_form
    }
    return render(request, "signin.html", context)


# ======================
#       Profile
# ======================
def profile(request):
    return render(request, "profile.html")


# ======================
#    Profile Edit
# ======================
def edit_profile(request):
    return render(request, "edit-profile.html")