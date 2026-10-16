from django.shortcuts import render, get_object_or_404
from accounts.models import Profile
from projects.models import Project, ProjectMember
from interactions.models import JoinRequest, Follow, Like
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Exists, OuterRef, Q, Count


# get posts
def get_posts(owner_name = None, following = None, ai_matched = None, limit = None, user = None):
    projects = Project.objects.select_related(
        "owner_name", "owner_name__profile"
    ).prefetch_related(
        "required_skills"
    ).annotate(
        members_count=Count("members", distinct=True),
        likes_count=Count("likes", distinct=True)
    )
    if owner_name:
        projects =  projects.filter(owner_name=owner_name)

    if following:
        projects = projects.filter(owner_name__followers__follower = following)
    if user and user.is_authenticated:
        liked_projects = Like.objects.filter(
            project = OuterRef("pk"),
            user = user
        )
        projects = projects.annotate(is_liked=Exists(liked_projects))
    return projects.order_by("-id")


# Home Page
def discover(request):  
    suggested_users = User.objects.exclude(username = request.user.username)
    request_count = 0
    feed = request.GET.get("feed", "all")
    if feed == "following":
        projects = get_posts(following=request.user, user=request.user)
    
    elif feed == "ai_matched":
        projects = get_posts(user=request.user, ai_matched=None)
    else:
        projects = get_posts(user=request.user)
    
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
        
# Search Results Page
def search_results(request):
    q = request.GET.get('q')

    if q:
        terms = q.split()
        project_vector = SearchVector(
            "title", 
            "desc", 
            "required_skills__name", 
            "category", 
            "overview"
        ) 
        user_vector = SearchVector(
            "username", 
            "first_name", 
            "last_name", 
            "profile__headline", 
            "profile__skills__name",
            "profile__location"
        )
        
        query = SearchQuery(
            " & ".join(f"{term}:*" for term in terms),
            search_type="raw"
        )
        print(query)
        
        projects = get_posts().annotate(
            rank=SearchRank(
                project_vector, 
                query
            )
        ).filter(
            rank__gte=0.001
        ).order_by(
            "-rank", 
            "id"
        ).distinct()

        people = User.objects.annotate(
            rank=SearchRank(user_vector, query)
        ).select_related(
            "profile"    
        ).filter(
            rank__gte=0.001
        ).order_by(
            "-rank"
        ).distinct()
        
        
        projects_count = projects.count()
        people_count = people.count()
    else :
        projects = None
        people = None
        projects_count = 0
        people_count = 0
    
    total_results = projects_count + people_count
    context = {
        "projects" : projects,
        "people" : people,
        "q": q,
        "projects_count" :projects_count,
        "people_count" : people_count,
        "total_results" : total_results
    }
        
    return render(request, 'search-results.html', context)
    

#Dashboard Page
def dashboard(request):
    return render(request, "index.html")


def messages(request):
    return render(request, "messages.html")


def notifications(request):
    return render(request, "notifications.html")



