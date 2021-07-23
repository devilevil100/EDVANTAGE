from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, blank=False)


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, blank=False)
    resume = models.FileField(upload_to ='uploads/resume/')
    degree = models.FileField(upload_to ='uploads/degree/')
    verify = models.FileField(upload_to ='uploads/verify/')
    approved = models.BooleanField(default=False)

class Room(models.Model):
    name = models.CharField(max_length=50, blank=False)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False)
    

    