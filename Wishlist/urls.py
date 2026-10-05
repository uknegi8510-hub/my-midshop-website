from django.urls import path,include
from Wishlist import views

#here to give path

urlpatterns = [
    path('wishlist/',views.wishlist_page,name="wishlist")
]