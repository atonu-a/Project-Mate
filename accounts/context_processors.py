from .models import Profile
from interactions.models import JoinRequest
from realtime_actions.models import Notification


def profile_context(request):
    request_count = 0
    unread_notification_count = 0
    
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(
            user=request.user
        )
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
        "profile": profile,
        "request_count" : request_count,
        "unread_notification_count" : unread_notification_count
    }