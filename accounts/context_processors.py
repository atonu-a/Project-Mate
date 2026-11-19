from .models import Profile
from interactions.models import JoinRequest
from realtime_actions.models import Notification
from projects.models import Project
from django.db.models import Q
from django.contrib.auth.models import User
from interactions.models import Follow

def profile_context(request):

    request_count = 0
    user = request.user if request.user.is_authenticated else None
    unread_notification_count = 0
    profile = None
    suggested_users = User.objects.exclude(username = user).select_related("profile").prefetch_related("profile__skills")[:3]
    
    if user:
        profile = getattr(request, "profile", None
        )
        following_users = Follow.objects.filter(follower = user).values_list("following_id", flat=True)
        suggested_users = User.objects.exclude(id__in = following_users).exclude(username = user).select_related("profile").prefetch_related("profile__skills")[:3]
        for teammate in suggested_users:
            print(teammate.username,list(teammate.profile.skills.values_list("name", flat=True))
    )
        if profile is None:
            profile, _ = Profile.objects.get_or_create(user = request.user)
        request_count = JoinRequest.objects.filter(
            project__owner_name=request.user,
            status="Pending"
        ).count()
        unread_notification_count = Notification.objects.filter(
            recipient = request.user,
            is_read = False
        ).count()
        
    else:
        profile = None

    return {
        'user': user,
        "profile": profile,
        "suggested_users": suggested_users,
        "request_count" : request_count,
        "unread_notification_count" : unread_notification_count
    }