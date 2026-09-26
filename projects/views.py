from django.shortcuts import render, get_object_or_404
from .models import Project
from accounts.models import Profile


def project_detail(request, slug):
    project = get_object_or_404(Project, slug = slug)
  
    context = {

        "project" : project
        }
    return render(request, "project-detail.html",context)
# Create your views here.
