from rest_framework import serializers
from Cart.models import Cart
from Products.models import Product

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','product','quantity']
        

