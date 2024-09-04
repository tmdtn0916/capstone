from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class StoryRequest(models.Model):
    keywords = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keywords

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), name=name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        user = self.create_user(email, name, phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # password 해싱을 위해 충분한 길이 설정
    phone = models.CharField(max_length=20)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email', 'password']

    def save(self, *args, **kwargs):
        if self.pk is None: #새 객체 생성 시에만 해싱
            self.set_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'user'