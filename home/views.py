from django.shortcuts import render, get_object_or_404
from accounts.models import Profile
from projects.models import Project, ProjectMember
from interactions.models import JoinRequest, Follow
from django.contrib.auth.models import User

# Create your views here.
# get posts
def get_posts(owner_name = None, following = None, ai_matched = None, limit = None):
    if owner_name:
        return Project.objects.filter(owner_name = owner_name).order_by("-id")
    if following:
        return Project.objects.filter(owner_name__followers__follower = following).order_by("-id")
    return Project.objects.all().order_by("-id")


# Home Page
def discover(request):
    
    suggested_users = User.objects.exclude(username = request.user.username)
    request_count = 0
    # is_following =False
    
    feed = request.GET.get("feed", "all")
    if feed == "following":
        projects = get_posts(following=request.user)
    
    elif feed == "ai_matched":
        projects = get_posts(ai_matched=None)
    else:
        projects = get_posts()
    
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower = request.user).values_list("following_id", flat=True)
        suggested_users = User.objects.exclude(id__in = following_users).exclude(username = request.user.username)
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
        "feed" : feed,
        "suggested_users" : suggested_users,
    }
    
    return render(request, "discover.html", context)
        


#Dashboard Page
def dashboard(request):
    return render(request, "index.html")


def messages(request):
    return render(request, "messages.html")


def notifications(request):
    return render(request, "notifications.html")



