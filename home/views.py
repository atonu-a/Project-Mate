from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Profile
from projects.models import Project, ProjectMember
from interactions.models import JoinRequest, Follow, Like, Save, Comment
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Exists, OuterRef, Q, Count, Value, BooleanField, Prefetch


# Landing Page
def landing_page(request):
    return render(request, "landing.html")


# get posts
def get_posts(owner_name = None, following = None, recommended = None, limit = None, user = None,exclude_own=False,):
    projects = Project.objects.select_related(
        "owner_name", "owner_name__profile"
    ).prefetch_related(
        "required_skills",
        Prefetch(
            "comments",
            queryset=Comment.objects.select_related(
                "user",
                "user__profile"
            ).order_by("-created_at"),
            to_attr="prefetched_comments"
        )
    ).annotate(
        members_count=Count("members", distinct=True),
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comments", distinct=True)
    )
    if user and exclude_own:
        projects = projects.exclude(owner_name=user)
    if owner_name:
        projects =  projects.filter(owner_name=owner_name).order_by("-id")

    if following:
        projects = projects.filter(owner_name__followers__follower = following).order_by("-id")
    
        
    if user:
        followed_users = Follow.objects.filter(
            follower = user,
            following = OuterRef("owner_name")
        )
        projects = projects.annotate(is_following=Exists(followed_users))
        liked_projects = Like.objects.filter(
            project = OuterRef("pk"),
            user = user
        )
        projects = projects.annotate(is_liked=Exists(liked_projects)).order_by("-id")
        
        saved_projects = Save.objects.filter(
            project = OuterRef("pk"),
            user = user
        )
        projects = projects.annotate(is_saved = Exists(saved_projects)).order_by("-id")
        
    if recommended and user:
        user_skill_ids = user.profile.skills.values_list(
            "id", flat = True
        )
        projects = projects.annotate(
            matched_skills = Count(
                'required_skills', filter=Q(
                    required_skills__id__in = user_skill_ids
                ), distinct=True
            ),
            total_required_skills = Count(
                'required_skills',
                distinct=True
            )
        )
        projects = list(projects)
        
        for project in projects:
            if project.total_required_skills:
                project.skill_match = round(
                    project.matched_skills / project.total_required_skills *100
                )
            else :
                project.skill_match = 0
        projects.sort(
            key=lambda p:p.skill_match, reverse=True
        )
        
    return projects


# feed Page
def discover(request):  
    user  = request.user if request.user.is_authenticated else None
    recommended = True if request.user.is_authenticated else None

    suggested_users = User.objects.exclude(username = user)
    request_count = 0
    feed = request.GET.get("feed", "all")
    
    if feed == "following":
        projects = get_posts(following=user, user=user, recommended=recommended)
    
    elif feed == "recommended":
        projects = get_posts(user=user, recommended=recommended, exclude_own=True)
    else:
        projects = get_posts(user=user, recommended=recommended)
    
    if user:
        following_users = Follow.objects.filter(follower = user).values_list("following_id", flat=True)
        suggested_users = User.objects.exclude(id__in = following_users).exclude(username = user).select_related("profile")
        
        
        project_ids = [project.id for project in projects]
        member_project_ids = set(ProjectMember.objects.filter(
            project_id__in = project_ids,
            user = user
        ).values_list("project_id", flat=True))
        join_requests = {}

        for jr in JoinRequest.objects.filter(
            project_id__in=project_ids,
            user=user
        ).order_by("-id"):
            join_requests.setdefault(jr.project_id, jr)
        for project in projects:
            project.is_following = project.owner_name_id in following_users
            project.is_member = (project.id in member_project_ids)

            project.join_request = (join_requests.get(project.id))
        request_count = JoinRequest.objects.filter(
            project__owner_name=user,
            status="Pending"
        ).count()        
    context = {
        "projects": projects,
        "request_count" : request_count,
        "feed" : feed,
        "suggested_users" : suggested_users,
    }
    
    return render(request, "discover.html", context)
 
 
# Home Page
def home(request):
    if not request.user.is_authenticated:
        return redirect("overview")
    else :
        return redirect("discover")


# Search Results Page
def search_results(request):
    q = request.GET.get('q')
    user = request.user if request.user.is_authenticated else None
    recommended = True if request.user.is_authenticated else None
    if user:
        followed_users = Follow.objects.filter(
            follower = user,
            following=OuterRef("pk")
        )
        follow_status = Exists(followed_users)

    else:
        follow_status = Value(False, output_field=BooleanField())

    if q:
        terms = q.split()
        project_vector = SearchVector(
            "title", 
            "desc", 
            "required_skills__name", 
            "category", 
            "overview", 
            "owner_name__username",
            "owner_name__first_name",
            "owner_name__last_name",
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
        
        projects = get_posts(user=user).annotate(
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
            rank=SearchRank(user_vector, query),
            is_following = follow_status
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
    


def about(request):
    return render(request, "about.html")

#Dashboard Page
def dashboard(request):
    return render(request, "index.html")


def messages(request):
    return render(request, "messages.html")




