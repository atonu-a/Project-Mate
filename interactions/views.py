from django.shortcuts import render, redirect, get_object_or_404
from accounts.views import signin
from .models import JoinRequest
from projects.views import project_detail
from projects.models import Project, ProjectMember
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

# ===========================
#   Join Request Sending
# ===========================
@login_required(login_url="signin")
def send_request(request, slug):
    project = get_object_or_404(Project, slug = slug)
    
    if request.method == "POST":
        
        # Already Member?
        already_member = ProjectMember.objects.filter(project = project, user = request.user).exists()
        if already_member:
            messages.error(request, "You are already a member of this project!")
            return redirect("project_detail", slug=slug)
        
        
        # Already Requested?
        already_requested = JoinRequest.objects.filter(project=project, user=request.user, status="Pending").exists()       
        if already_requested:
            return redirect("project_detail", slug=slug)
        
        JoinRequest.objects.create(
            project = project,
            user = request.user
        )
        messages.success(request, "Join request sent!")
        
        
    return redirect("project_detail", slug=slug)

# ===========================
#   Join Request Checking
# ===========================
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

def reject_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    
    
    if join_request.project.owner_name != request.user:
        return redirect("requests")
    
    if request.method == "POST":
        
        join_request.status = "Rejected"
        messages.success(request, f"Rejected request from {join_request.user.first_name} {join_request.user.last_name}")
        join_request.save()
        
    return redirect("requests")