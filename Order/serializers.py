from django import forms
from Accounts.models import Address
from Order.models import ShippingAddress
from rest_framework import serializers



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'full_name',
            'phone',
            'address_line',
            'city',
            'state',
            'pincode',
            'country',
            'address_type',
            'is_default',
        ]
        read_only_fields = ['id']

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
