from django.db import models
from django.conf import settings
from Products.models import Product

# Create your models here.
class Wishlist(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wishlist")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="wishlist")
    quantity=models.CharField(max_length=2,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['user','product'],
                name="unique_user_product_wishlist"
            )
        ]
   