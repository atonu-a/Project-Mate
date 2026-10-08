from django.shortcuts import render, get_object_or_404
from accounts.models import Profile
from projects.models import Project

# Create your views here.
# get posts
def get_posts(owner_name = None):
    if owner_name:
        return Project.objects.filter(owner_name = owner_name).order_by("-id")
    return Project.objects.all().order_by("-id")


# Home Page
def discover(request):
    projects = get_posts()
    context = {
        "projects": projects,
    }
    
    return render(request, "discover.html", context)
        


#Dashboard Page
def dashboard(request):
    return render(request, "index.html")


def messages(request):
    return render(request, "messages.html")


def notifications(request):
    return render(request, "notifications.html")



