from django.db import models
from django.conf import settings
from Products.models import Product
# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    class Meta:
       constraints = [
           models.UniqueConstraint(
               fields=["user", "product"],
               name="unique_user_product_cart"
           )
       ]

    def __str__(self):
        return f"{self.user} - {self.product}"


