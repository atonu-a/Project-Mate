from datetime import datetime, time

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_date
from .models import Project, ProjectMember, Task
from accounts.models import Profile
from accounts.views import signin
from interactions.models import JoinRequest, Comment
from interactions.utils import attach_comment_tree
from home.views import discover
from django.db.models import Q, Exists, OuterRef, Count, Prefetch



# ======================
#       Project Details
# ======================
def project_detail(request, slug):
    user = request.user if request.user.is_authenticated else False
    join_request = JoinRequest.objects.filter(
        project=OuterRef("pk"),
        user = user
    ).order_by("-created_at") 
    membership = ProjectMember.objects.select_related("user", "user__profile").filter(
        project=OuterRef("pk"),
        user=user
    )
    project = get_object_or_404(
        (Project.objects.prefetch_related(
            "members__user__profile", "required_skills",
            Prefetch(
                "comments",
                queryset=Comment.objects.select_related(
                    "user", "user__profile"
                ).order_by("created_at"),
                to_attr="all_comments"
            )
        ).annotate(
            has__join__request = Exists(join_request),
            is_member = Exists(membership),
            members_count=Count("members", distinct=True),
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True)
        )), slug=slug
    )
    attach_comment_tree(project)
    
    latest_join_request = None

    if user:
        latest_join_request = JoinRequest.objects.filter(
            project=project,
            user=request.user
        ).order_by("-created_at").first()

    context = {
        "members" : project.members.all(),
        "project" : project,
        "projects" : [project],
        "join_request" : latest_join_request,
        "is_member" : project.is_member
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
            return render(request, "edit-project.html")
            
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
        return redirect("project_detail", slug=slug)
        
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
@login_required(login_url="signin")
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
@login_required(login_url="signin")
def my_projects(request):
    # owned_projects = Project.objects.all().filter(owner_name = request.user) 
    # joined_projects = Project.objects.filter()
    projects = Project.objects.filter(
        Q(owner_name = request.user) |
        Q(members__user = request.user)
    ).distinct().select_related(
        "owner_name", "owner_name__profile"
    ).prefetch_related(
        "members__user", "members__user__profile"
    ).annotate(
        members_count=Count("members", distinct=True),
    )
    
    total_projects = projects.count()

    context= {
        "projects" : projects,
        "total_projects" : total_projects
    }
    return render(request, 'my-projects.html', context)



@login_required(login_url="signin")
def task_assign(request):
    if request.method == "POST":
        project = get_object_or_404(
            Project.objects.prefetch_related("members"),
            pk=request.POST.get("project"),
        )

        if request.user != project.owner_name:
            messages.error(request, "You are not authorized to assign tasks for this project.")
            return redirect("task_view")

        assigned_to = get_object_or_404(
            ProjectMember,
            pk=request.POST.get("member"),
            project=project,
        )
        assigned_by = get_object_or_404(
            ProjectMember,
            project=project,
            user=request.user,
        )

        title = request.POST.get("title", "").strip()
        desc = request.POST.get("desc", "").strip()
        deadline = parse_date(request.POST.get("deadline", ""))
        if not title or not deadline:
            messages.error(request, "Project, member, title, and deadline are required.")
            return redirect("task_view")
        deadline = timezone.make_aware(
            datetime.combine(deadline, time.min),
            timezone.get_current_timezone(),
        )

        Task.objects.create(
            project=project,
            assigned_to=assigned_to,
            assigned_by=assigned_by,
            title=title,
            desc=desc,
            deadline=deadline,
        )
        messages.success(
            request,
            f"Task assigned to {assigned_to.user.get_full_name() or assigned_to.user.username}",
        )
        return redirect("task_view")

    return redirect("task_view")




def task_view(request):
    projects = Project.objects.none()
    if request.user.is_authenticated:
        projects = Project.objects.filter(
            owner_name=request.user
        ).prefetch_related(
            "members__user"
        )

    project_members_json = {}
    for project in projects:
        project_members_json[str(project.pk)] = [
            {
                "id": member.pk,
                "name": member.user.get_full_name() or member.user.username,
            }
            for member in project.members.select_related("user").all()
        ]

    return render(
        request,
        "task-management.html",
        {
            "projects": projects,
            "project_members_json": project_members_json,
        },
    )

    
    

    