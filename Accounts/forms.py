from django import forms
from Accounts.models import Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        fields = [
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