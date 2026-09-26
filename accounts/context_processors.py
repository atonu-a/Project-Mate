from .models import Profile


def profile_context(request):
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(
            user=request.user
        )
    else:
        profile = None

    return {
        "profile": profile,
    }