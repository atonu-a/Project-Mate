def profile_context(request):
    if request.user.is_authenticated:
        return {
            "profile": request.user.profile
        }

    return {
        "profile": None
    }