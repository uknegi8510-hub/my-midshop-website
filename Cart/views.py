from django.shortcuts import render
from .models import Cart
from django.contrib.auth.decorators import login_required
from Cart.models import Cart
from Products.models import Product
from Cart.serializers import AddToCartSerializer
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    totals = calculate_cart_total(cart_items)

    context = {
        "cart_items": cart_items,
        "step": 1,
        "totals": totals,
    }

    return render(request, "cart.html", context)

def calculate_cart_total(cart_items):
    subtotal=0
    
    for item in cart_items:
        subtotal +=item.product.price * item.quantity

    discount_percent=10
    discount=(subtotal * discount_percent)/100

    shipping=50
    total = subtotal - discount + shipping

    return {
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "total": total
    }

class AddToCartAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity')  
        if not product_id:
            return Response(
                {"error":"product_id is require"},
                status=status.HTTP_400_BAD_REQUEST
            )   
        try:
            product=Product.objects.get(
                id=product_id,
                is_available=True
            ) 
        except Product.DoesNotExist:
            return Response(
                {'error':"Product not found"},
                status=status.HTTP_404_NOT_FOUND

            )
        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart,created=Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                'quantity':quantity
            }
        )
        return Response(
            {
                'message':"Product added to cart",
                'created':created,

            },
            status=status.HTTP_201_CREATED
        )
            
class removeCartAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request):
        product_id=request.data.get('product_id')
        cart_item=Cart.objects.filter(
            user=request.user,
            product_id=product_id
            ).first()
        if not cart_item:
            return Response(
                {'error':"product is not exsite"},
                status=status.HTTP_404_NOT_FOUND

            )
        cart_item.delete()
        return Response(
            {"message":"Product remove from wishlist"},
            status=status.HTTP_200_OK
        )

    
@login_required
def address_page(request):

    cart_items = Cart.objects.filter(user=request.user)

    totals = calculate_cart_total(cart_items)

    request.session["cart_totals"] = {
        "subtotal": float(totals["subtotal"]),
        "discount": float(totals["discount"]),
        "shipping": float(totals["shipping"]),
        "total": float(totals["total"]),
    }

    context = {
        "cart_items": cart_items,
        "totals": totals,
        "step": 2,
    }

    return render(request, "address.html", context)