from django.shortcuts import render, get_object_or_404
from Products.models import Product, Category, Brand


def home(request):
    brand = Brand.objects.filter(is_active=True)
    category = Category.objects.filter(is_active=True)
    product_data = Product.objects.filter(is_available=True)

    context = {
        "brand": brand,
        "category": category,
        "product_data": product_data
    }

    return render(request, 'index.html', context)


def product_page(request, slug):
    product_id = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    related_product = Product.objects.filter(
        category=product_id.category,
        is_available=True
    ).exclude(
        id=product_id.id
    )[:10]

    context = {
        "data": product_id,
        "related_product": related_product
    }

    return render(request, 'product_page.html', context)


# Category products
def product_listing(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True
    )

    product_data = Product.objects.filter(
        category=category,
        is_available=True
    )

    context = {
        "product_data": product_data,
        "category": category,
    }

    return render(request, 'product_listing.html', context)


# Brand products
def brand_product_listing(request, slug):
    brand = get_object_or_404(
        Brand,
        slug=slug,
        is_active=True
    )

    product_data = Product.objects.filter(
        brand_name=brand,
        is_available=True
    )

    context = {
        "product_data": product_data,
        "brand": brand,
    }

    return render(request, 'product_listing.html', context)