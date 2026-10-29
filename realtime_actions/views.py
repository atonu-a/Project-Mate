from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="signin")
def notification_view(request):
    notifications = Notification.objects.filter(
        recipient = request.user
    )
    
    context = {
        "notifications" : notifications
    }
    return render(request, "notifications.html", context)