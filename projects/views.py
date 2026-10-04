from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project
from accounts.models import Profile
from accounts.views import signin
from home.views import discover


# ======================
#       Project Details
# ======================
def project_detail(request, slug):
    project = get_object_or_404(Project, slug = slug)  
    context = {

        "project" : project
        }
    return render(request, "project-detail.html",context)


# ======================
#   Project Creation 
# ======================
# views.py
@login_required(login_url="signin")
def create_project(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        status = request.POST.get("status")
        raw_skills = request.POST.get("required_skills")
        team_size = request.POST.get("team_size")
        deadline = request.POST.get("deadline")
        category = request.POST.get("category")
        img = request.FILES.get("img")
        overview = request.POST.get("overview")
        compensation_type = request.POST.get("compensation_type")
        payment_details = request.POST.get("payment_details")
        
        if compensation_type == "Paid" and not payment_details:
            messages.error(request, "Please enter payment details!")
            return render(request, "create-project.html")
            
        if compensation_type != "Paid":
            payment_details = 0
            
        project = Project.objects.create(
            owner_name = request.user,
            title = title,
            desc = desc,
            status = status,
            team_size = team_size,
            deadline = deadline,
            category = category,
            img = img,
            overview = overview,
            compensation_type = compensation_type,
            payment_amount = payment_details,
        )
        
        if raw_skills:

            skill_names = [s.strip() for s in raw_skills.split(',') if s.strip()]
            
            skill_objects = []
            for name in skill_names:

                from .models import Skill 
                skill_obj, created = Skill.objects.get_or_create(name__iexact=name, defaults={'name': name})
                skill_objects.append(skill_obj)
            
            project.required_skills.set(skill_objects)
        
        messages.success(request, "Project created successfully!")
        return redirect("home")
        
    return render(request, "create-project.html")
