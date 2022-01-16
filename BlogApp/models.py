from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.conf import settings




class CustomUser(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(unique=True)
        first_name=models.CharField(max_length=264)
        last_name=models.CharField(max_length=264)
        mobile_no=models.CharField(max_length=10)
        is_verified = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        objects = CustomUserManager()

        def __str__(self):
            return self.email

# Create your models here.
class ContactUs(models.Model):
    serialno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=264)
    phone=models.CharField(max_length=13)
    email=models.EmailField()
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)
    objects=models.Manager


class Post(models.Model):
    serialno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=264)
    content = models.TextField()
    author = models.CharField(max_length=264)
    slug = models.CharField(max_length=264)
    timestamp = models.DateTimeField(blank=True)
    objects=models.Manager

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    serialno = models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CharField,null=True)
    timestamp=models.DateTimeField(default=now)
    objects=models.Manager
