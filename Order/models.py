from django.db import models
from django.conf import settings


# Create your models here.

class Order(models.Model):
    STATUS_CHOICES=[
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('processing',"processing"),
        ('shipped','shipped'),
        ('delivered',"delivered"),
        ('cancelled','cancelled')
    ]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_number=models.CharField(max_length=30,default='', unique=True,blank=True,null=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey('Products.Product',on_delete=models.PROTECT)
    product_name=models.CharField(max_length=255,default='',null=True,blank=True)
    quantity = models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    subtotal=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"


class ShippingAddress(models.Model):
    ADDRESS_TYPE = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="shipping_address"
    )

    full_name = models.CharField(max_length=150, default='', null=True, blank=True)
    phone = models.CharField(max_length=15, default='', null=True, blank=True)
    address_line = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, default='', null=True, blank=True)
    state = models.CharField(max_length=100, default='', null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, default='India', null=True, blank=True)
    address_type = models.CharField(max_length=20,choices=ADDRESS_TYPE,default='home')

    def __str__(self):
        return f"{self.full_name} - {self.city}"


class Payment(models.Model):

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD = [
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Wallet'),
    ]

    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='payment')
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='pending')
    razorpay_order_id = models.CharField(max_length=255,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=255,blank=True,null=True)
    razorpay_signature = models.CharField(max_length=255,blank=True,null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"