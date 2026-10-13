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


# Follow model
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'following')
    
    
    def __str__(self) :
        return f"{self.follower.username} follows {self.following.username}"
    
# Post react model
class Like(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    created_at =models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f"{self.user.username} liked {self.project.title}"