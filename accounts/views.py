from django.shortcuts import render, redirect
from .forms import RegistrationForm
# Create your views here.
# ======================
#       Registrantion
# ======================

def signup(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
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
#       Login
# ======================
def signin(request):
    return render(request, "signin.html")


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