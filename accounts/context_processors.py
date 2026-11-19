from .models import Profile
from interactions.models import JoinRequest
from realtime_actions.models import Notification
from projects.models import Project
from django.db.models import Q


def profile_context(request):

    request_count = 0
    user = request.user if request.user.is_authenticated else None
    unread_notification_count = 0
    profile = None
    
    if user:
        profile = getattr(request, "profile", None
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
        "request_count" : request_count,
        "unread_notification_count" : unread_notification_count
    }