from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from  Accounts.Manager import UserManager
from django.db import models
from django.conf import settings


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


class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile') 
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    profile_image = models.ImageField(upload_to='profiles/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Address(models.Model):

    ADDRESS_TYPE = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='addresses')   
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100,default='India')
    address_type = models.CharField( max_length=20, choices=ADDRESS_TYPE, default='home')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_type} - {self.city}"

