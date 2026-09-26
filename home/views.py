from django.shortcuts import render, get_object_or_404
from accounts.models import Profile
from projects.models import Project

# Create your views here.
# Home Page
def discover(request):
    projects = Project.objects.all()
    context = {
        "projects": projects,
    }
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user)
        context["profile"] = profile

    
    
    return render(request, "discover.html", context)
        
    

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




def my_projects(request):
    return render(request, 'my-projects.html')


def notifications(request):
    return render(request, "notifications.html")



