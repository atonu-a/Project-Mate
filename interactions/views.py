from django.shortcuts import render, redirect, get_object_or_404
from accounts.views import signin
from .models import JoinRequest, Follow
from projects.views import project_detail
from projects.models import Project, ProjectMember
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

# Create your views here.

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

    if member_count >= join_request.project.team_size:
        join_request.status = "Rejected"
        join_request.save()
        messages.error(request, "Team is already full. Request rejected")
        return redirect("requests")
    
    if join_request.project.owner_name != request.user:
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


@login_required(login_url="signin")

def toggle_follow(request, username):
    
    if request.method=='POST':
        targeted_user = get_object_or_404(User, username=username)

        if request.user == targeted_user:
            return redirect("public_profile", username=username)

        follow, created = Follow.objects.get_or_create(
            follower = request.user, 
            following = targeted_user

        )
        messages.success(request, f"Followed {targeted_user.first_name} {targeted_user.last_name}")
        
        if not created :
            follow.delete()
            messages.success(request, f"Unfollowed {targeted_user.first_name} {targeted_user.last_name}")
    return redirect("public_profile", username=username)