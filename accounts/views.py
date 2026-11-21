from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.views.decorators.cache import never_cache
from .models import *
from projects.models import Project, ProjectMember
from interactions.models import JoinRequest
from home.views import get_posts
from interactions.models import Follow
from django.db.models import Count, Q
from datetime import timedelta




# ======================
#       Registration
# ======================
@never_cache
def signup(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.first_name = user_form.cleaned_data.get('first_name')
            user.last_name = user_form.cleaned_data.get('last_name')
            user.email = user_form.cleaned_data.get('email')
            
            user.save()
            login(request, user)
            messages.success(request, "Account created and logged in successfully!")
            return redirect('complete_profile')
    
    else:
        user_form = RegistrationForm()
    
    context = {
        'user_form':user_form
    }
    
    return render(request, "signup.html", context)


# ======================
#  Profile Completeion
# ======================
@login_required(login_url="signin")
def complete_profile(request):
    profile, created = Profile.objects.get_or_create(
        user = request.user
    )
    if request.method == "POST":
        profile.headline = request.POST.get("headline", "")
        profile.whatsapp = request.POST.get("whatsapp","")
        profile.linkedin = request.POST.get("linkedin","")
        profile.location = request.POST.get("location","")
        profile.url = request.POST.get("url","")
        profile.institute = request.POST.get("institute", "")
        profile.github = request.POST.get("github", "")
        profile.bio = request.POST.get("bio", "")

        
        profile_pic = request.FILES.get("profile_pic")
        if profile_pic:
            profile.profile_pic = profile_pic
        cover_pic = request.FILES.get("cover_pic")
        if cover_pic:
            profile.cover_pic = cover_pic
        
        
        profile.save()
        
        selected_fields = request.POST.get("fields", "")
        profile.fields.clear()
        
        if selected_fields:
            field_names = selected_fields.split(",")

            for field_name in field_names:
                field, created = Field.objects.get_or_create(
                    name=field_name.strip()
                )

                profile.fields.add(field)
                
                
        skills = request.POST.get("skills", "")

        profile.skills.clear()

        if skills:
            skill_names = skills.split(",")

            for skill_name in skill_names:
                skill, created = Skill.objects.get_or_create(
                    name=skill_name.strip()
                )

                profile.skills.add(skill)
                
        messages.success(request, "Profile Edited Successfully.")
        return redirect("profile", request.user.username)
    
    context = {
        "profile":profile
    }
    
    
    return render(request, "profile-setup.html", context)


# ======================
#       Signout
# ======================
@login_required(login_url="signin")
def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('signin')


# ======================
#       Signin
# ======================
def signin(request):
    redirect_url = request.META.get('HTTP_REFERER', '/')
    if request.method == "POST":
        user_form = AuthenticationForm(request, data=request.POST)
        if user_form.is_valid():
            user = user_form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
       
    else:
        user_form = AuthenticationForm()
       
    context = {
        'user_form':user_form
    }
    return render(request, "signin.html", context)


# ======================
#     User  Profile
# ======================
def profile(request, username ):

    profile = get_object_or_404(
        Profile.objects.select_related('user').annotate(
            followers_count=Count('user__followers', distinct=True),
            following_count=Count('user__following', distinct=True)
        ), 
        user__username=username
    )
    user = profile.user
    projects = get_posts(user, user=user)
    is_following = False
    followers_count = profile.followers_count
    following_count = profile.following_count
    
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile.user).exists()
        project_ids = [project.id for project in projects]
        member_ids = set(ProjectMember.objects.filter(
            project_id__in = project_ids,
            user = request.user
        ).values_list("project_id", flat=True))
        
        join_requests = {
            join_request.project_id : join_request
            for join_request in JoinRequest.objects.filter(
                project_id__in = project_ids,
                user = request.user
            ).order_by("-id")
        }
        
        for project in projects:
            project.is_following = is_following
            project.is_member = (project.id in member_ids)
            project.join_request = (join_requests.get(project.id))
        
        
        if request.user !=user:
            today = timezone.now().date()
            already = ProfileView.objects.filter(profile = user.profile, viewer = request.user, viewed_at = today).exists()
            
            if not already:
                ProfileView.objects.create(profile=user.profile, viewer=request.user)
        
    context = {
        "projects": projects,
        "project_count": projects.count(),
        "date_joined": user.date_joined,
        # "is_following": is_following,
        "followers_count" : followers_count,
        "following_count" : following_count,
    }

    if request.user == user:
        context["profile"] = profile
        return render(request, "profile.html", context)

    context.update({
        "public_profile": user,
        "is_following" : is_following

    })
    return render(request, "public-profile.html", context)


# ======================
#    Profile Edit
# ======================
@login_required(login_url="signin")
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    selected_fields = list(
        profile.fields.values_list("name", flat=True)
    )

    if request.method == "POST":

        # Full Name
        full_name = request.POST.get("full_name", "").strip()
        name_parts = full_name.split(" ", 1)

        request.user.first_name = name_parts[0] if name_parts else ""
        request.user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        request.user.save()

        # Profile information
        profile.headline = request.POST.get("headline", "")
        profile.whatsapp = request.POST.get("whatsapp", "")
        profile.linkedin = request.POST.get("linkedin", "")
        profile.location = request.POST.get("location", "")
        profile.url = request.POST.get("url", "")
        profile.institute = request.POST.get("institute", "")
        profile.github = request.POST.get("github", "")
        profile.bio = request.POST.get("bio", "")

        # Profile picture
        profile_pic = request.FILES.get("profile_pic")
        cover_pic = request.FILES.get("cover_pic")

        if profile_pic:
            profile.profile_pic = profile_pic
        
        if cover_pic:
            profile.cover_pic = cover_pic

        profile.save()

        # Fields
        profile.fields.clear()

        fields = request.POST.get("fields", "")

        if fields:
            for field_name in fields.split(","):
                field_name = field_name.strip()

                if field_name:
                    field, created = Field.objects.get_or_create(
                        name=field_name
                    )
                    profile.fields.add(field)

        # Skills
        profile.skills.clear()

        skills = request.POST.get("skills", "")

        if skills:
            for skill_name in skills.split(","):
                skill_name = skill_name.strip()

                if skill_name:
                    skill, created = Skill.objects.get_or_create(
                        name=skill_name
                    )
                    profile.skills.add(skill)

        messages.success(request, "Profile updated successfully.")

        return redirect("profile", request.user.username)

    return render(request, "edit-profile.html", {
        "profile": profile,
        "selected_fields": selected_fields,
    })       
    
    
# ======================
#    Dashboard
# ======================

@login_required(login_url="signin")
def dashboard(request):
    user = request.user
    profile = user.profile
    now = timezone.now()
    
    # Skill matches
    my_ids = set(profile.skills.values_list("id", flat=True))
    open_projects = (Project.objects.filter(status="Open").exclude(owner_name=user).prefetch_related("required_skills"))
    scores = []
    for p in open_projects:
        req = {s.id for s in p.required_skills.all()}
        
        if req & my_ids:
            scores.append(len(req & my_ids) / len(req))
    skill_matches = len(scores)
    top_match = round(max(scores)* 100) if scores else 0
     
    # +N this month
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_this_month = (
        Project.objects.filter(owner_name=user, create_at__gte=month_start.date()).count()
        + ProjectMember.objects.filter(user=user, joined_at__gte=month_start)
            .exclude(project__owner_name=user).count()
    )
    
    
    # Trending projects/posts
    top_projects = projects = Project.objects.select_related(
            "owner_name", "owner_name__profile"
        ).prefetch_related(
            "required_skills"
        ).annotate(
            members_count=Count("members", distinct=True),
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True)
        ).order_by("-likes_count", "-id")[:2]
    
    # Total Projects of user
    total_projects = projects.count()
    
    
    # Profile Views Count
    views = ProfileView.objects.filter(profile=profile)
    
    week_ago, two_weeks_ago = now - timedelta(days=7), now - timedelta(days=14)
    
    views_this_week = views.filter(viewed_at__gte = week_ago).count()
    views_last_week = views.filter(viewed_at__gte = two_weeks_ago,viewed_at__lt=week_ago).count()
    views_change = (round((views_this_week - views_last_week) / views_last_week * 100)
        if views_last_week else None)
    

    context = {
        'total_projects' : total_projects,
        'top_projects' : top_projects,
        "total_views" : views.count(),
        "views_this_week" : views_this_week,
        "views_change": views_change,
        "new_this_month": new_this_month,
        "skill_matches": skill_matches,
        "top_match": top_match
    }
    return render(request, "dashboard.html", context)