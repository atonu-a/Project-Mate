from django.shortcuts import render, get_object_or_404
from accounts.models import Profile
from projects.models import Project, ProjectMember
from interactions.models import JoinRequest, Follow
from django.contrib.auth.models import User

# Create your views here.
# get posts
def get_posts(owner_name = None, following = None, ai_matched = None, limit = None):
    projects = Project.objects.select_related(
        "owner_name", "owner_name__profile"
    ).prefetch_related(
        "required_skills"
    )
    if owner_name:
        projects =  projects.filter(owner_name=owner_name)

    if following:
        projects = projects.filter(owner_name__followers__follower = following)
    return projects.order_by("-id")


# Home Page
def discover(request):  
    suggested_users = User.objects.exclude(username = request.user.username)
    request_count = 0
    feed = request.GET.get("feed", "all")
    if feed == "following":
        projects = get_posts(following=request.user)
    
    elif feed == "ai_matched":
        projects = get_posts(ai_matched=None)
    else:
        projects = get_posts()
    
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower = request.user).values_list("following_id", flat=True)
        suggested_users = User.objects.exclude(id__in = following_users).exclude(username = request.user.username).select_related("profile")
        
        
        project_ids = [project.id for project in projects]
        member_project_ids = set(ProjectMember.objects.filter(
            project_id__in = project_ids,
            user = request.user
        ).values_list("project_id", flat=True))
        join_requests = {
            join_request.project_id: join_request
            for join_request in JoinRequest.objects.filter(
                project_id__in = project_ids,
                user = request.user
            ).order_by("-id")
        }
        for project in projects:
            project.is_following = project.owner_name_id in following_users
            project.is_member = (project.id in member_project_ids)

            project.join_request = (join_requests.get(project.id))
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



