from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from Products.models import Product
from Wishlist.models import Wishlist

# Create your views here.
@login_required
def wishlist_page(request):
    wishlist_items=Wishlist.objects.filter(user=request.user)
    context={
        "wishlist_items":wishlist_items,
    }

        
    return render(request,'wishlist.html',context)

class AddToWishlistAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        product_id=request.data.get("product_id")
        quantity=request.data.get('quantity')
        if not product_id:
            return Response(
                {'error':"product_id is required"},
                status=status.HTTP_400_BAD_REQUEST

            )
        try:
            product=Product.objects.get(
                id=product_id,
                is_available=True
                )
        except Product.DoesNotExist:
            return Response(
                {"error":"product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if quantity < 1:
            return Response(
                {"error":"quantity must be at least 1"},
                status=status.HTTP_404_NOT_FOUND
            )
        wishlist_page,created=Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                'quantity':quantity
            }
        )
        
        return Response(
            {
            'message':"Prodcut added to wishlist",
            "created":created,
            },
            status=status.HTTP_201_CREATED
        )

class WishlistDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request):
        product_id=request.data.get('product_id')
        wishlist_item=Wishlist.objects.filter(
            user=request.user,
            product_id=product_id
            ).first()
        if not wishlist_item:
            return Response(
                {'error':"product is not exsite"},
                status=status.HTTP_404_NOT_FOUND

            )
        wishlist_item.delete()
        return Response(
            {"message":"Product remove from wishlist"},
            status=status.HTTP_200_OK
        )