from django.urls import include,path
from Cart.views import *
from Cart import views



urlpatterns = [
    path("cart/",views.cart , name="cart"),
    path("checkout/address/",views.address_page ,name="address_page"),
]
