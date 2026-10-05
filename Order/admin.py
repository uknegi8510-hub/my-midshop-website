from django.contrib import admin
from Order.models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=['user', 'total_amount','created_at']

admin.site.register(Order,OrderAdmin)
