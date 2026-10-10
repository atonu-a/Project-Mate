from .models import Profile
from interactions.models import JoinRequest


def profile_context(request):
    request_count = 0
    
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(
            user=request.user
        )
        request_count = JoinRequest.objects.filter(
            project__owner_name=request.user,
            status="Pending"
        ).count()
    else:
        profile = None

    return {
        "profile": profile,
        "request_count" : request_count
    }