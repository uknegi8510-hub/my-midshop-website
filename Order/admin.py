from django.contrib import admin
from Order.models import Order, ShippingAddress, Payment, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'order_number',
        'status',
        'total_amount',
        'created_at'
    ]

    search_fields = (
        'order_number',
        'user__email',
        'user__display_name',
    )

    list_filter = ('status', 'created_at')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order',
        'product_name',
        'quantity',
        'price',
        'subtotal'
    ]

    search_fields = (
        'order__order_number',
        'product_name',
    )


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'full_name',
        'phone',
        'city',
        'state',
        'pincode'
    ]

    search_fields = (
        'order__order_number',
        'full_name',
        'phone',
        'city',
        'pincode',
    )


class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'payment_method',
        'amount',
        'status',
        'razorpay_payment_id',
        'created_at',
    )

    list_filter = (
        'payment_method',
        'status',
    )

    search_fields = (
        'order__order_number',
        'razorpay_payment_id',
        'razorpay_order_id',
    )

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Payment, PaymentAdmin)