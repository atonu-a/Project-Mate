from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    
    def __str__(self) :
        return self.name
class Field(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    
    def __str__(self) :
        return self.name

    
class Profile(models.Model):
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles")
    headline = models.CharField(max_length=255, blank=True)
    fields = models.ManyToManyField(Field, related_name="profiles", blank=True)
    skills = models.ManyToManyField(Skill, related_name="profiles", blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    
    profile_pic = models.ImageField(upload_to='images',blank=True, null=True, default="/static/images/default.svg")
    
    
    def __str__(self) :
        return self.user.username
    

    
    

    