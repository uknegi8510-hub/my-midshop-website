from django.contrib import admin
from Cart.models import Cart

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity']

admin.site.register(Cart,CartAdmin)

