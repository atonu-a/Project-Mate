from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Skills(models.Model):
    name = models.CharField(max_length=255)
    
    
    def __str__(self) :
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='images',blank=True, null=True, default="/static/images/default.svg")
    first_name = models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    url = models.TextField()
    skills = models.ManyToManyField(Skills)
    
    
    
    def __str__(self) :
        return self.user.username
    

    
    

    