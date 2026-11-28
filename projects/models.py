from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from accounts.models import Skill


class Project(models.Model):
    
    STATUS = (
        ("Open", "Open"),
        ("In_Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Closed", "Closed"),
    )
    
    COMPENSATION = (
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
        ("Negotiable", "Negotiable"),      
    )
    
    
    owner_name = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from = "title", unique=True, max_length=255, always_update=False)
    desc = models.TextField()
    status = models.CharField(choices=STATUS, max_length=20, default="Open")
    required_skills = models.ManyToManyField(Skill, related_name="projects")
    team_size = models.PositiveBigIntegerField(default=1)
    deadline = models.DateField(null= True, blank=True)
    category = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to="images", blank=True, null=True)
    overview = models.TextField()
    
    compensation_type = models.CharField(choices=COMPENSATION,max_length=20, default="Unpaid")
    payment_amount = models.IntegerField( null=True, blank=True)

    
    
    def save(self, *args, **kwargs):
    #    if not self.slug:
    #        self.slug = slugify(self.title)
       super().save(*args, **kwargs) # Call the real save() method
       
    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})
    def __str__(self):
            return self.title
    
 
class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships" )
    joined_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=100)
        
    
class Task(models.Model):
    STATUS = (
        ("Assigned", "Assigned"),
        ("Submitted", "Submitted"),
        ("Verified", "Verified"),
        ("Rejected", "Rejected"),
    )
    
    
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(ProjectMember, on_delete=models.SET_NULL, related_name="tasks", blank=True, null=True)
    assigned_by = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    status = models.CharField(choices=STATUS, default="Assigned")
    
    def __str__(self):
        return self.title
    
    
    
