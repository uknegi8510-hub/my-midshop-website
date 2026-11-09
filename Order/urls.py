from django.urls import path
from Order import views

urlpatterns = [
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order/adress/<int:order_id>/',views.order_address, name='checkout_address'),
    path('order/adress/save/<int:order_id>/',views.save_order_address, name='save_order_address'),
    path('order/adress/checkout/<int:order_id>/',views.order_summery, name='order_checkout'),
    path('order/adress/checkout/payment/<int:order_id>/',views.payment_page,name='order_payment'),
    path('payment/create/<int:order_id>/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payment/verify/<int:order_id>/', views.verify_razorpay_payment, name='verify_razorpay_payment'),
    path('payment/cod/<int:order_id>/', views.place_cod_order, name='place_cod_order'),
    path('order/success/<int:order_id>/',views.order_success,name='order_success'),



]