from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required
from home.utils import time_ago
# Create your views here.

@login_required(login_url="signin")
def notification_view(request):
    notifications = Notification.objects.filter(
        recipient = request.user
    )
    for notice in notifications:
        notice.created_at_ago = time_ago(notice.created_at)
    
    context = {
        "notifications" : notifications
    }
    return render(request, "notifications.html", context)