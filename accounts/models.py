from django.db import models
from django.contrib.auth.models import User

DEFAULT_PROFILE_PIC_URL = (
    "https://res.cloudinary.com/ddrochzoq/image/upload/default_mdzqdy.svg"
)

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
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    headline = models.CharField(max_length=255, blank=True)
    fields = models.ManyToManyField(Field, related_name="profiles", blank=True)
    skills = models.ManyToManyField(Skill, related_name="profiles", blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True, default="Remote")
    institute = models.CharField(max_length=100, blank=True, null=True, default="Independent")
    url = models.URLField(blank=True, null=True)
    bio = models.CharField(blank=True, null=True, max_length=150)
    github = models.URLField(blank=True, null=True)
    whatsapp = models.CharField()
    linkedin = models.URLField(blank=True, null=True)
    
    profile_pic = models.ImageField(upload_to='images',blank=True, null=True,  default="default_mdzqdy.svg")
    cover_pic = models.ImageField(upload_to='images', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.profile_pic:
            self.profile_pic = 'default_mdzqdy.svg'
        super().save(*args, **kwargs)

    @property
    def profile_pic_url(self):
        if (
            not self.profile_pic
            or self.profile_pic.name.rsplit("/", 1)[-1] == "default_mdzqdy.svg"
        ):
            return DEFAULT_PROFILE_PIC_URL
        return self.profile_pic.url

    def __str__(self) :
        return self.user.username
    

    
    

    