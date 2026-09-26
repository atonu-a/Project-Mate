from django.shortcuts import render, get_object_or_404
from accounts.models import Profile
from projects.models import Project

# Create your views here.
# Home Page
def discover(request, slug):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
        return render(request, "discover.html", {"profile":profile})
    else:
        projects = get_object_or_404(Project, slug=slug)
        return render(request, "discover.html", {"projects":projects})
        
    

#Dashboard Page
def dashboard(request):
    return render(request, "index.html")

#Creation page
def create(request):
    return render(request, "create-project.html")

# My Projects page
def requests(request):
    return render(request, "requests.html")


def messages(request):
    return render(request, "messages.html")


def project_detail(request, project_id=None):
    return render(request, "project-detail.html", {"project_id": project_id})


def my_projects(request):
    return render(request, 'my-projects.html')


def notifications(request):
    return render(request, "notifications.html")



