from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.views.decorators.cache import never_cache
from .models import *
# Create your views here.
# ======================
#       Registrantion
# ======================
@never_cache
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
@login_required
def complete_profile(request):
    profile, created = Profile.objects.get_or_create(
        user = request.user
    )
    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name","")
        request.user.last_name = request.POST.get("last_name","")
        request.user.save()
        
        
        profile.headline = request.POST.get("headline", "")
        profile.location = request.POST.get("location","")
        profile.url = request.POST.get("url","")
        profile.institute = request.POST.get("institute", "")
        profile.github = request.POST.get("github", "")
        profile.bio = request.POST.get("bio", "")

        
        profile_pic = request.FILES.get("profile_pic")
        if profile_pic:
            profile.profile_pic = profile_pic
        
        
        profile.save()
        
        selected_fields = request.POST.get("fields", "")
        profile.fields.clear()
        
        if selected_fields:
            field_names = selected_fields.split(",")

            for field_name in field_names:
                field, created = Field.objects.get_or_create(
                    name=field_name.strip()
                )

                profile.fields.add(field)
                
                
        skills = request.POST.get("skills", "")

        profile.skills.clear()

        if skills:
            skill_names = skills.split(",")

            for skill_name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    name=skill_name.strip()
                )

                profile.skills.add(skill)
                
        messages.success(request, "Profile Edited Successfully.")
        return redirect("profile")
    
    context = {
        "profile":profile
    }
    
    
    return render(request, "profile-setup.html", context)


# ======================
#       Signout
# ======================
@login_required
def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
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
    profile = Profile.objects.get(user = request.user)
    context = {
        "profile":profile
    }
    return render(request, "profile.html", context)


# ======================
#    Profile Edit
# ======================
@login_required(login_url="signin")
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    selected_fields = list(
        profile.fields.values_list("name", flat=True)
    )

    if request.method == "POST":

        # Full Name
        full_name = request.POST.get("full_name", "").strip()
        name_parts = full_name.split(" ", 1)

        request.user.first_name = name_parts[0] if name_parts else ""
        request.user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        request.user.save()

        # Profile information
        profile.headline = request.POST.get("headline", "")
        profile.location = request.POST.get("location", "")
        profile.url = request.POST.get("url", "")
        profile.institute = request.POST.get("institute", "")
        profile.github = request.POST.get("github", "")
        profile.bio = request.POST.get("bio", "")

        # Profile picture
        profile_pic = request.FILES.get("profile_pic")

        if profile_pic:
            profile.profile_pic = profile_pic

        profile.save()

        # Fields
        profile.fields.clear()

        fields = request.POST.get("fields", "")

        if fields:
            for field_name in fields.split(","):
                field_name = field_name.strip()

                if field_name:
                    field, created = Field.objects.get_or_create(
                        name=field_name
                    )
                    profile.fields.add(field)

        # Skills
        profile.skills.clear()

        skills = request.POST.get("skills", "")

        if skills:
            for skill_name in skills.split(","):
                skill_name = skill_name.strip()

                if skill_name:
                    skill, created = Skill.objects.get_or_create(
                        name=skill_name
                    )
                    profile.skills.add(skill)

        messages.success(request, "Profile updated successfully.")

        return redirect("profile")

    return render(request, "edit-profile.html", {
        "profile": profile,
        "selected_fields": selected_fields,
    })       