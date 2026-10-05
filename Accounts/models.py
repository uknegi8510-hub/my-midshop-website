from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from  Accounts.Manager import UserManager


# Create your views here.
class User(AbstractUser):
    username=None
    email= models.EmailField(unique=True)
    display_name=models.CharField(max_length=100,null=True,blank=True)
    is_verified=models.BooleanField(default=None,null=True,blank=True)
    register_otp=models.CharField(max_length=6,null=True,blank=True)
    login_otp=models.CharField(max_length=6,null=True,blank=True)
    last_login_time=models.DateTimeField(null=True, blank=True)
    email_verification_token=models.CharField(max_length=255,default="",null=True,blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    EMAIL_FIELD="email"

    objects=UserManager()
    def __str__(self):
        return f"{self.display_name or 'User'} - {self.email}"


