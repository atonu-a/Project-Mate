import json
from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification, FirebaseInstallation
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_protect

from home.utils import time_ago
from .push import send_test_push

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


@require_GET
def firebase_messaging_service_worker(request):
    worker_path = settings.BASE_DIR / "static" / "firebase-msg-sw.js"
    response = FileResponse(
        worker_path.open("rb"),
        content_type="application/javascript",
    )
    response["Cache-Control"] = "no-cache"
    return response



@login_required(login_url="signin")
@require_POST
@csrf_protect
def save_firebase_token(request):

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    if not isinstance(data, dict):
        return JsonResponse({"error": "A JSON object is required"}, status=400)

    fcm_token = data.get("fcm_token")
    if (
        not isinstance(fcm_token, str)
        or not fcm_token.strip()
        or len(fcm_token) > 4096
    ):
        return JsonResponse(
            {"error": "A valid FCM token is required"},
            status=400
        )

    FirebaseInstallation.objects.update_or_create(
        fcm_token=fcm_token,
        defaults={
            "user": request.user
        }
    )

    push_error = send_test_push(fcm_token)
    if push_error:
        return JsonResponse({"error": push_error}, status=503)

    return JsonResponse({
        "success": True,
        "message": "Browser registered and Firebase accepted a test notification."
    })