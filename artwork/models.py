from django.db import models
from django.contrib.auth.models import User

class Artwork(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="artworks")
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='artworks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ai_status = models.CharField(max_length=50, default="Pending")
    ai_score = models.IntegerField(default=0)
    ai_strengths = models.TextField(blank=True)
    ai_weaknesses = models.TextField(blank=True)
    ai_suggestions = models.TextField(blank=True)
    

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# Create your models here.
