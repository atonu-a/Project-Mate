from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Exists
from accounts.views import signin
from home.views import get_posts
from .models import JoinRequest, Follow, Like, Save, Comment
from projects.views import project_detail
from projects.models import Project, ProjectMember
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

# ===========================
#   Join Request Sending
# ===========================
@login_required(login_url="signin")
def send_request(request, slug):
    project = get_object_or_404(Project, slug = slug)
    next_url = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = project.get_absolute_url()
    
    if request.method == "POST":
        
        # Already Member?
        already_member = ProjectMember.objects.filter(project = project, user = request.user).exists()
        if already_member:
            messages.error(request, "You are already a member of this project!")
            return redirect(next_url)
        
        
        # Already Requested?
        already_requested = JoinRequest.objects.filter(project=project, user=request.user, status="Pending").exists()       
        if already_requested:
            return redirect(next_url)
        
        JoinRequest.objects.create(
            project = project,
            user = request.user,
            msg = request.POST.get("msg", "")
        )
        messages.success(request, "Join request sent!")
        
        
    return redirect(next_url)

# ===========================
#   Join Request Checking
# ===========================
@login_required(login_url="signin")
def join_requests(request):
    requests = JoinRequest.objects.filter(
        project__owner_name = request.user,
        status="Pending"
    ).select_related("user", "project")
    context = {
        "requests" : requests,
    }
    
    
    return render(request, "requests.html", context)


# ===========================
#   Join Request Accepting
# ===========================
@login_required(login_url="signin")
def accept_request(request, request_id):
    
    
    join_request = get_object_or_404(JoinRequest, id=request_id)
    member_count = ProjectMember.objects.filter(
        project=join_request.project
        ).count()
    
    if join_request.project.owner_name != request.user:
            return redirect("requests")
        
        
    if member_count >= join_request.project.team_size:
        join_request.status = "Rejected"
        join_request.save()
        messages.error(request, "Team is already full. Request rejected")
        return redirect("requests")
    
    
    if request.method == "POST":
        ProjectMember.objects.create(
            project = join_request.project,
            user = join_request.user,
            role = "Member"
        )
        
        join_request.status = "Accepted"
        messages.success(request, f"Accepted request from {join_request.user}")
        join_request.save()
        
    return redirect("requests")



# ===========================
#   Join Request Rejecting
# ===========================
@login_required(login_url="signin")
def reject_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    
    
    if join_request.project.owner_name != request.user:
        return redirect("requests")
    
    if request.method == "POST":
        
        join_request.status = "Rejected"
        messages.success(request, f"Rejected request from {join_request.user.first_name} {join_request.user.last_name}")
        join_request.save()
        
    return redirect("requests")


# ===========================
#   Remove a Member
# ===========================
def remove_member(request, slug, username):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        

        member = get_object_or_404(ProjectMember, project=project, user__username = username)

        is_owner = project.owner_name == request.user 
        if not is_owner:
            messages.error(request, "You are not authorized to remove anyone from a project.")
            return redirect("project_detail", slug=project.slug)
        if member.user == project.owner_name:
            messages.error(request, "You cannot leave from your own project.")
            return redirect("project_detail", slug=project.slug)
        member.delete()
        JoinRequest.objects.filter(
            project = project,
            user = member.user,
            status = "Accepted"
        ).update(status = "Cancelled")
        
        messages.success(request, f"You have successfully removed {member.user.username}")

    return redirect("project_detail", slug=project.slug)



# ===========================
#   Leave From a Project
# ===========================
@login_required(login_url="signin")
def leave_project(request, slug):
    if request.method == "POST":
        user = request.user
        project = get_object_or_404(Project, slug=slug)
        is_owner = project.owner_name == user
        is_member = ProjectMember.objects.filter(
            project=project,
            user= user
        ).exists()

        if is_member:
            if is_owner:
                messages.error(request, "You cannot leave from your own project!")
                return redirect("project_detail", slug)

            else :
                project.members.get(user=user).delete()
                JoinRequest.objects.filter(
                    project = project,
                    user = user,
                    status = "Accepted"
                    ).update(status = "Cancelled")
                messages.success(request, "You left the team!")
                return redirect("project_detail", slug)
        
        else :
            messages.error(request,"You are not member of this project!")
        
    return redirect("project_detail", slug)
  
    
# ===========================
#   Following an User
# ===========================
@login_required(login_url="signin")
def toggle_follow(request, username):
    redirect_url = request.META.get('HTTP_REFERER', '/')
    if request.method=='POST':
        targeted_user = get_object_or_404(User, username=username)

        if request.user == targeted_user:
            return redirect(redirect_url, username=username)

        follow, created = Follow.objects.get_or_create(
            follower = request.user, 
            following = targeted_user

        )
        if created:
            messages.success(request, f"Followed {targeted_user.first_name} {targeted_user.last_name}")
        
        if not created :
            follow.delete()
            messages.success(request, f"Unfollowed {targeted_user.first_name} {targeted_user.last_name}")
    return redirect(redirect_url, username=username)


# ===========================
#   Like/Dislike to a post
# ===========================

def like_project(request, slug):
    if not request.user.is_authenticated:
        return JsonResponse({
            "success":False,
            "login_required":True,
            "login_url":f"/signin/?next={request.path}"
        }, status=401)
        
    project = get_object_or_404(Project, slug = slug)    
    if request.method == "POST":
        project = get_object_or_404(Project, slug = slug)
        
        like, created = Like.objects.get_or_create(
            project = project,
            user = request.user
        )
        
        if not created:
            like.delete()
            
        is_liked = project.likes.filter(user = request.user).exists()
    return JsonResponse({
        "success" : True,
        "liked" : created,
        "likes_count" : project.likes.count(),
        "is_liked" : is_liked
    })
      

# ===========================
#   Save/Unsave a Post
# ===========================
def save_project(request, slug):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return JsonResponse({
            "success" : False,
            "login_required" :True,
            "login_url":f"/signin/?next={request.path}"
        }, status = 401)
        
    project = get_object_or_404(Project, slug = slug)    
    if request.method == "POST":
        
        
        save, created = Save.objects.get_or_create(
            project = project,
            user = user
        )
        if created:
            msg = "Project saved!"
        
        if not created:
            save.delete()
            msg="Project unsaved!"
            
        is_saved = project.saves.filter(user = user).exists()
   
    return JsonResponse({
        "success" : True,
        "saved" : created,
        "is_saved" : is_saved,
        "msg" : msg
    })


# ===========================
#   View Saved Page
# ===========================
@login_required(login_url="signin")
def saved_page(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        projects = get_posts(user=user).filter(is_saved = True)
        
    context = {
        "projects" : projects
    }
    return render(request, "saved.html" ,context)



# ===========================
#   Comment on a Post
# ===========================

@login_required(login_url="signin")
def create_comment(request, slug):
    user = request.user if request.user.is_authenticated else None
    
    if not user:
        return JsonResponse({
            "success" : False,
            "login_required" : True,
            "login_url" : f"/signin/?next={request.path}"
        }, status=401)
        
    project = get_object_or_404(Project, slug = slug)
    if request.method == "POST":
        project = get_object_or_404(Project, slug = slug)
        input_comment = request.POST.get("input_comment", "").strip()
        
        comment = Comment.objects.create(
            user = user,
            project = project,
            commented_text = input_comment
        )
        
        return JsonResponse({
            "success" : True,
            "comment" : {
                "id" : comment.id,
                "commented_text" : comment.commented_text,
                "project": comment.project.slug,
                "full_name": (
                    f"{comment.user.first_name} "
                    f"{comment.user.last_name}"
                ).strip(),
                "profile_pic" : (
                    comment.user.profile.profile_pic_url
                ),

                "created_at" : comment.created_at.isoformat(),
                
            }
        }, status=201)
        
        