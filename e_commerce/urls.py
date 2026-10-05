"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from Products import views 
from django.conf.urls.static import static
from Accounts.views import *
from Cart.views import  *
from Wishlist.views import  *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('',include('Products.urls')),
    path('',include("Accounts.urls")),
    path('',include("Cart.urls")),
    path('',include("Wishlist.urls")),
    path('register/',RegisterAPI.as_view()),
    path('verify/',VerifyRegisterOTP.as_view()),
    path('login_otp/',LoginAPIView.as_view()),
    path('login_verify/',VerifyLoginOTP.as_view()),
    path('add-cart/', AddToCartAPIView.as_view()),
    path("cart-remove/",removeCartAPIView.as_view()),
    path('add-wishlist/', AddToWishlistAPIView.as_view()),
    path('add-wishlist/remove/',WishlistDeleteAPIView.as_view()),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

