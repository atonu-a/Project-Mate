from django.shortcuts import render
from accounts.models import *

# Create your views here.
# Home Page
def discover(request):

        
    return render(request, "discover.html")

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



