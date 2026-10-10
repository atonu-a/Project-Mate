from django.shortcuts import render, get_object_or_404
from accounts.models import Profile
from projects.models import Project, ProjectMember
from interactions.models import JoinRequest

# Create your views here.
# get posts
def get_posts(owner_name = None):
    if owner_name:
        return Project.objects.filter(owner_name = owner_name).order_by("-id")
    return Project.objects.all().order_by("-id")


# Home Page
def discover(request):
    projects = get_posts()
    request_count = 0
    if request.user.is_authenticated:
        for project in projects:
            project.is_member = ProjectMember.objects.filter(
                project=project,
                user=request.user
            ).exists()

            project.join_request = JoinRequest.objects.filter(
                project=project,
                user=request.user
            ).order_by("-created_at").first()
        request_count = JoinRequest.objects.filter(
            project__owner_name=request.user,
            status="Pending"
        ).count()        
    context = {
        "projects": projects,
        "request_count" : request_count,
    }
    
    return render(request, "discover.html", context)
        


#Dashboard Page
def dashboard(request):
    return render(request, "index.html")


def messages(request):
    return render(request, "messages.html")


def notifications(request):
    return render(request, "notifications.html")



