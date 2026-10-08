from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models import Project

# Create your models here.
class JoinRequest(models.Model):
    
    STATUS = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled")
    )
    
    
    project = models.ForeignKey(Project, related_name="request", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="requested", on_delete=models.CASCADE)
    msg = models.CharField(blank=True, null=True, max_length=255)
    status = models.CharField(choices=STATUS, max_length=20, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)
