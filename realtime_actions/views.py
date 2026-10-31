from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from home.utils import time_ago
# Create your views here.


# ==============================
#       Notification page
# ==============================
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


# ==============================
#       read/unread check
# ==============================
@login_required(login_url="signin")
def read_notice(request, pk):
    notification = get_object_or_404(
        Notification, pk=pk, recipient = request.user
    )
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return redirect(notification.target_url)



# ==============================
#    Mark all as read/unread
# ==============================
@login_required(login_url="signin")
def mark_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(
            recipient = request.user,
            is_read = False,
        ).update(is_read=True)
        
    return redirect("notifications")