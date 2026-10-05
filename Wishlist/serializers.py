from rest_framework import serializers
from Wishlist.models import Wishlist
from Products.models import Product

class AddToWishlist(serializers.ModelSerializer):
    class Meta:
        model=Wishlist
        fields=['id','product','quantity']


