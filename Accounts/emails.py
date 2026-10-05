from  django.core.mail import send_mail
import random
from django.conf import settings
from .models import User

# Create your emails here.

def send_register_otp(email):
    subject=f"your account verifications email"
    otp=random.randint(1000,9999)
    message=f"your otp is {otp}"
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj=User.objects.get(email=email)
    user_obj.register_otp=otp
    user_obj.save()


def send_login_otp(email):
    subject=f"your account verifications email"
    otp=random.randint(1000,9999)
    message=f"your otp is {otp}"
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj=User.objects.get(email=email)
    user_obj.login_otp=otp
    user_obj.save()