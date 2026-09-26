from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Skill

class Project(models.Model):
    
    STATUS = (
        ("Open", "Open"),
        ("In_Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Closed", "Closed"),
    )
    
    owner_name = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from = "title", unique=True, max_length=255)
    desc = models.TextField()
    status = models.CharField(choices=STATUS, max_length=20, default="Open")
    required_skills = models.ManyToManyField(Skill, related_name="projects")
    team_size = models.PositiveBigIntegerField(default=1)
    deadline = models.DateField(null= True, blank=True)
    category = models.CharField(max_length=100)
    create_at = models.DateField(auto_now_add=True)
    img = models.ImageField(upload_to="images", blank=True, null=True)
    overview = models.TextField()
    
    
    
    def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.title)
       super().save(*args, **kwargs) # Call the real save() method
       
    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})
    def __str__(self):
            return self.title
    
    
    
# Create your models here.
