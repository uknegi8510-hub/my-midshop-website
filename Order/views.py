from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from Products.models import Product
from Order.models import Order, OrderItem
import uuid
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Accounts.models import Address,UserProfile,User
from django.db import transaction
from Order.serializers import AddressSerializer
from Accounts.forms import *
from django.http import HttpResponseBadRequest
from decimal import Decimal,ROUND_HALF_UP
from Order.models import ShippingAddress,Payment
from django.views.decorators.http import require_http_methods
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from decimal import Decimal
from django.urls import reverse


razorpay_client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)
def calculate_order_totals(items):
    subtotal = Decimal("0.00")

    for item in items:
        price = Decimal(str(item["price"]))
        quantity = int(item["quantity"])

        if price < 0 or quantity < 1:
            raise ValueError("Invalid order item price or quantity.")

        subtotal += price * quantity

    subtotal = subtotal.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    discount = (subtotal * Decimal("0.10")).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    shipping = Decimal("50.00")
    total = subtotal - discount + shipping

    return {
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "total": total,
    } 

@login_required
def buy_now(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    try:
        quantity = int(request.GET.get("quantity", 1))
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Invalid quantity.")

    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        return redirect("product_page", product.slug)

    # Use the price retrieved from the database.
    unit_price = Decimal(str(product.price))

    totals = calculate_order_totals([
        {
            "price": unit_price,
            "quantity": quantity,
        }
    ])

    with transaction.atomic():

        # Find a pending order belonging to this user
        # that contains exactly this one product.
        pending_orders = (
            Order.objects
            .filter(
                user=request.user,
                status="pending",
                items__product=product,
            )
            .distinct()
            .order_by("-id")
        )

        order = None

        for candidate in pending_orders:
            order_items = list(candidate.items.all())

            if (
                len(order_items) == 1
                and order_items[0].product_id == product.id
            ):
                order = candidate
                break

        if order is None:
            order = Order.objects.create(
                user=request.user,
                order_number=(
                    f"ORD-{uuid.uuid4().hex[:10].upper()}"
                ),
                total_amount=totals["total"],
                status="pending",
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=unit_price,
                quantity=quantity,
                subtotal=unit_price * quantity,
            )

        else:
            item = order.items.get(product=product)

            item.product_name = product.name
            item.price = unit_price
            item.quantity = quantity
            item.subtotal = unit_price * quantity
            item.save()

            order.total_amount = totals["total"]
            order.save(update_fields=["total_amount"])

    return redirect("checkout_address",order_id=order.id,)


@login_required
def save_order_address(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if request.method != "POST":
        return redirect("checkout_address", order_id=order.id)

    form = AddressForm(request.POST)

    if form.is_valid():
        with transaction.atomic():
            address = form.save(commit=False)
            address.user = request.user

            existing_addresses = Address.objects.filter(
                user=request.user
            )

            if not existing_addresses.exists():
                address.is_default = True
            elif address.is_default:
                existing_addresses.filter(
                    is_default=True
                ).update(is_default=False)

            address.save()

        return redirect(
            "checkout_address",
            order_id=order.id
        )

    # If validation fails, show the errors on the same page.
    addresses = Address.objects.filter(
        user=request.user
    ).order_by("-is_default", "-updated_at")

    return render(
        request,
        "Order/order_address.html",  # Use your actual template path
        {
            "order": order,
            "addresses": addresses,
            "form": form,
            "step": 1,
        }
    )

@login_required
@require_http_methods(["GET", "POST"])
def order_address(request, order_id):
    order = get_object_or_404(Order,id=order_id,user=request.user)
    addresses = Address.objects.filter(user=request.user).order_by("-is_default", "-created_at")
    if request.method == "POST":
        address_id = request.POST.get("selected_address")
        if not address_id:
            items = [
                {"price": item.price, "quantity": item.quantity}
                for item in order.items.all()
            ]

            context = {
                "order": order,
                "addresses": addresses,
                "step": 1,
                "error": "Please select a delivery address.",
                **calculate_order_totals(items),
            }

            return render(
                request,
                "order_pages/order_address.html",
                context
            )

        # Verify the address belongs to the logged-in user.
        address = get_object_or_404(
            Address,
            id=address_id,
            user=request.user
        )

        # Copy the selected address into ShippingAddress.
        with transaction.atomic():
            ShippingAddress.objects.update_or_create(
                order=order,
                defaults={
                    "full_name": address.full_name,
                    "phone": address.phone,
                    "address_line": address.address_line,
                    "city": address.city,
                    "state": address.state,
                    "pincode": address.pincode,
                    "country": address.country,
                    "address_type": address.address_type,
                }
            )

        return redirect("order_checkout",order_id=order.id)

    # GET request: display the address page.
    items = [
        {"price": item.price, "quantity": item.quantity}
        for item in order.items.all()
    ]
    context = {"order": order,"addresses": addresses,"step": 1,**calculate_order_totals(items),}
    return render(request,"order_pages/order_address.html",context)



@login_required
def order_summery(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = order.items.all()

    shipping_address = ShippingAddress.objects.filter(
        order=order
    ).first()

    if not shipping_address:
        return redirect(
            'checkout_address',
            order_id=order.id
        )

    items = [
        {
            "price": item.price,
            "quantity": item.quantity
        }
        for item in order_items
    ]

    totals = calculate_order_totals(items)

    order.total_amount = totals["total"]
    order.save(update_fields=["total_amount"])

    context = {
        "order": order,
        "order_items": order_items,
        "shipping_address": shipping_address,
        **totals,
        "step": 2,
    }

    return render(request,"order_pages/order_checkout.html",context)

@login_required
def payment_page(request, order_id):

    order = get_object_or_404(Order,id=order_id,user=request.user)

    shipping_address = ShippingAddress.objects.filter(order=order).first()

    if not shipping_address:
        return redirect(
            'checkout_address',
            order_id=order.id
        )

    if order.status != 'pending':
        return redirect(
            'order_success',
            order_id=order.id
        )

    order_items = order.items.all()

    items = [
        {
            "price": item.price,
            "quantity": item.quantity
        }
        for item in order_items
    ]

    totals = calculate_order_totals(items)

    context = {
        "order": order,
        "order_items": order_items,
        "shipping_address": shipping_address,
        **totals,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }
    return render(request,'order_pages/order_payment.html',context)

@login_required
@require_POST
def create_razorpay_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status != "pending":
        return JsonResponse(
            {"error": "This order cannot be paid."},
            status=400
        )

    shipping_address = ShippingAddress.objects.filter(
        order=order
    ).first()

    if not shipping_address:
        return JsonResponse(
            {"error": "Please select a delivery address first."},
            status=400
        )

    payment_method = request.POST.get("payment_method")

    allowed_methods = ["upi", "card", "netbanking", "wallet"]

    if payment_method not in allowed_methods:
        return JsonResponse(
            {"error": "Invalid payment method."},
            status=400
        )

    order_items = list(order.items.all())

    if not order_items:
        return JsonResponse(
            {"error": "Your order has no products."},
            status=400
        )

    try:
        totals = calculate_order_totals([
            {
                "price": item.price,
                "quantity": item.quantity
            }
            for item in order_items
        ])
    except (ValueError, TypeError):
        return JsonResponse(
            {"error": "Unable to calculate order amount."},
            status=400
        )

    total_amount = totals["total"]

    if total_amount <= 0:
        return JsonResponse(
            {"error": "Invalid payment amount."},
            status=400
        )

    # Razorpay accepts the amount in paise.
    amount_in_paise = int(total_amount * 100)

    try:
        razorpay_order = razorpay_client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": order.order_number,
            "notes": {
                "midshop_order_id": str(order.id),
                "customer_email": request.user.email,
            }
        })

        # Reuse the existing Payment record if one exists.
        payment, created = Payment.objects.update_or_create(
            order=order,
            defaults={
                "payment_method": payment_method,
                "status": "pending",
                "amount": total_amount,
                "razorpay_order_id": razorpay_order["id"],
                "razorpay_payment_id": None,
                "razorpay_signature": None,
            }
        )

        order.total_amount = total_amount
        order.save(update_fields=["total_amount"])

        return JsonResponse({
            "success": True,
            "key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"],
            "payment_method": payment_method,
            "payment_id": payment.id,
            "customer_name": shipping_address.full_name,
            "customer_phone": shipping_address.phone,
            "customer_email": request.user.email,
        })

    except Exception:
        return JsonResponse(
            {"error": "Unable to start payment. Please try again."},
            status=502
        )


@login_required
@require_POST
def verify_razorpay_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    payment = get_object_or_404(
        Payment,
        order=order
    )

    razorpay_payment_id = request.POST.get(
        "razorpay_payment_id"
    )

    razorpay_order_id = request.POST.get(
        "razorpay_order_id"
    )

    razorpay_signature = request.POST.get(
        "razorpay_signature"
    )

    if not all([
        razorpay_payment_id,
        razorpay_order_id,
        razorpay_signature
    ]):
        return JsonResponse(
            {"error": "Payment verification details are missing."},
            status=400
        )

    if payment.status == "paid":
        return JsonResponse({"success": True,"redirect_url": reverse(    "order_success",    args=[order.id])})

    if (
        payment.razorpay_order_id != razorpay_order_id
        or order.status != "pending"
    ):
        return JsonResponse(
            {"error": "Invalid payment or order."},
            status=400
        )

    try:
        # Verify Razorpay signature.
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        })

        # Fetch actual payment details from Razorpay.
        gateway_payment = razorpay_client.payment.fetch(
            razorpay_payment_id
        )

        expected_amount = int(
            payment.amount * 100
        )

        if (
            gateway_payment["order_id"] != razorpay_order_id
            or gateway_payment["amount"] != expected_amount
            or gateway_payment["currency"] != "INR"
            or gateway_payment["status"] != "captured"
        ):
            return JsonResponse(
                {"error": "Payment has not been successfully captured."},
                status=400
            )

        with transaction.atomic():

            locked_order = Order.objects.select_for_update().get(
                id=order.id,
                user=request.user
            )

            locked_payment = Payment.objects.select_for_update().get(
                order=locked_order
            )

            if locked_payment.status == "paid":
                return JsonResponse({
                    "success": True,
                    "message": "Payment already completed."
                })

            if (
                locked_payment.razorpay_order_id != razorpay_order_id
                or locked_order.status != "pending"
            ):
                return JsonResponse(
                    {"error": "Order payment state has changed."},
                    status=400
                )

            locked_payment.razorpay_payment_id = razorpay_payment_id
            locked_payment.razorpay_signature = razorpay_signature
            locked_payment.status = "paid"
            locked_payment.save()

            locked_order.status = "confirmed"
            locked_order.save(update_fields=["status", "updated_at"])

        return JsonResponse({
            "success": True,
            "message": "Payment successful.",
            "redirect_url": f"/order/success/{order.id}/"
        })

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse(
            {"error": "Payment signature verification failed."},
            status=400
        )

    except Exception:
        return JsonResponse(
            {"error": "Payment verification failed. Please contact support if money was deducted."},
            status=400
        )

@login_required
@require_POST
def place_cod_order(request, order_id):

    with transaction.atomic():

        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            user=request.user
        )

        if order.status != "pending":
            return JsonResponse(
                {"error": "This order cannot be confirmed."},
                status=400
            )

        if not ShippingAddress.objects.filter(order=order).exists():
            return JsonResponse(
                {"error": "Please select a delivery address."},
                status=400
            )

        order_items = list(order.items.all())

        if not order_items:
            return JsonResponse(
                {"error": "Your order has no products."},
                status=400
            )

        try:
            totals = calculate_order_totals([
                {
                    "price": item.price,
                    "quantity": item.quantity
                }
                for item in order_items
            ])
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Unable to calculate order amount."},
                status=400
            )

        existing_payment = Payment.objects.filter(
            order=order
        ).first()

        if existing_payment and existing_payment.status == "paid":
            return JsonResponse(
                {"error": "This order has already been paid."},
                status=400
            )

        Payment.objects.update_or_create(
            order=order,
            defaults={
                "payment_method": "cod",
                "status": "pending",
                "amount": totals["total"],
                "razorpay_order_id": None,
                "razorpay_payment_id": None,
                "razorpay_signature": None,
            }
        )

        order.total_amount = totals["total"]
        order.status = "confirmed"
        order.save(update_fields=["total_amount", "status", "updated_at"])

    redirect('order_pages/order_success.html')

    return JsonResponse({"success": True,"message": "Your COD order has been placed successfully.","redirect_url": f"/order/success/{order.id}/"})


@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    shipping_address = get_object_or_404(
        ShippingAddress,
        order=order
    )

    order_items = order.items.select_related('product').all()

    payment = Payment.objects.filter(order=order).first()

    return render(
        request,
        'order_pages/order_success.html',
        {
            'order': order,
            'order_items': order_items,
            'shipping_address': shipping_address,
            'payment': payment,
        }
    )