from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

class Meet(models.Model):
    starting_time=models.DateTimeField(auto_now_add=False)
    ending_time=models.DateTimeField(auto_now_add=False)
    meeting_link=models.URLField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return str(self.id)

class Profile(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    mobile=models.CharField(max_length=20)
    otp=models.CharField(max_length=6)
 
    def __str__(self):
        return self.username