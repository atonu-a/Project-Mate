from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

# Create your models here.


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        NEW_JOIN_REQUEST = "join_request", "New Join Request"
        REQUEST_ACCEPTED = "accepted", "Request Accepted"
        NEW_FOLLOWER = "follow", "New Follower"
        PROJECT_LIKE = "like", "Project Like"
        PROJECT_COMMENT = "comment", "Project Comment"
        TEAM_REMOVED = "team_removed", "Removed from Team"
        
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    actor= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    content= models.CharField(max_length=255)
    target_url = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.recipient} - {self.notification_type}"
    