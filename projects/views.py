from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectMember
from accounts.models import Profile
from accounts.views import signin
from interactions.models import JoinRequest
from home.views import discover



# ======================
#       Project Details
# ======================
def project_detail(request, slug):
    project = get_object_or_404(Project, slug = slug)  
    members = project.members.all()
    join_request = None
    is_member = False

    if request.user.is_authenticated:
        join_request = JoinRequest.objects.filter(
            project=project,
            user=request.user
        ).order_by("-created_at").first()

        is_member = ProjectMember.objects.filter(
            project=project,
            user=request.user
        ).exists()
    
    context = {
        "members" : members,
        "project" : project,
        "join_request" : join_request,
        "is_member" : is_member
        }
    return render(request, "project-detail.html",context)


# ======================
#   Project Creation 
# ======================

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
        
        ProjectMember.objects.create(
            project = project,
            user = request.user,
            role = "Owner",
            
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

# ======================
#   Project Editing 
# ======================

@login_required(login_url="signin")
def edit_project(request, slug):
    previous_page = request.META.get('HTTP_REFERER', 'home')
    
    project = get_object_or_404(Project, slug = slug)
    skills_string = ", ".join([skill.name for skill in project.required_skills.all()])
    status_list = ["Open", "In Progress", "Completed", "Closed"]
    selected_status = project.status
    comp_list = ["Unpaid", "Paid", "Negotiable"]
    selected_comp = project.compensation_type
    
    
    if (project.owner_name != request.user):
        messages.error(request, "You are not authorized to edit this post.")
        return redirect(previous_page)
    
    if request.method == 'POST':
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        selected_status = request.POST.get("status")
        raw_skills = request.POST.get("required_skills")
        team_size = request.POST.get("team_size")
        deadline = request.POST.get("deadline")
        category = request.POST.get("category")
        img = request.FILES.get("img")
        overview = request.POST.get("overview")
        selected_comp = request.POST.get("compensation_type")
        payment_details = request.POST.get("payment_details")
        
        if selected_comp == "Paid" and not payment_details:
            messages.error(request, "Please enter payment details!")
            return render(request, "create-project.html")
            
        if selected_comp != "Paid":
            payment_details = 0
        
        
        
        project.title = title
        project.desc = desc
        project.status = selected_status
        project.team_size = team_size if team_size else 1
        project.category = category
        project.overview = overview
        project.compensation_type = selected_comp
        project.payment_amount = payment_details
        
        if deadline:
            project.deadline = deadline
        else:
            project.deadline = None
        if img:
            project.img = img

        
        
        project.save()
        
        messages.success(request, "Project edited successfully!")
        return redirect("my_projects")
        
    context = {
        "project":project,
        "skills_string": skills_string,
        "status_list" : status_list,
        'status' : selected_status,
        "comp_list" : comp_list,
        "compensation_type" : selected_comp
    }
        
    return render(request, "edit-project.html", context)


# ======================
#   Project Deletion
# ======================
@login_required(login_url="sigin")
def delete_project(request, slug):
    project = Project.objects.get(slug=slug)
    previous_page = request.META.get('HTTP_REFERER', 'home')
    if project.owner_name == request.user:
        project.delete()
    else :
        messages.error(request, "You are not authorized to delete this project")
        return redirect(previous_page)
    messages.success(request, "Project deleted successfully.")
    
    return redirect(previous_page)

# ======================
#   My Projects 
# ======================
def my_projects(request):
    projects = Project.objects.all().filter(owner_name = request.user)
    context= {
        "projects" : projects
    }
    return render(request, 'my-projects.html', context)