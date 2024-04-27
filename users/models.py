from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profiles/', default='profiles/user-default.png')   # Goes into static/images/profiles to upload the pictures
    github_profile = models.CharField(max_length=200, blank=True, null=True)
    linkedin_profile = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['created']

    
    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    def __str__(self):
        return self.name
    
    def ready(self):
        import users.signals


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)   
    # even if one does not have an accnout he/she can send a message using name and email
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    # By default, we are not allowed to connect to same database twice, this will throw warnings.
    # To avoid that, we add 'related_name' this acts as a reference for us to indentify the model it is refering to

    
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']

