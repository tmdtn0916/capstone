from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class StoryRequest(models.Model):
    keywords = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keywords

class User(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # password 해싱을 위해 충분한 길이 설정
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'user'