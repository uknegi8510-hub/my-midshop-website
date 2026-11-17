from django.shortcuts import render, get_object_or_404
from Products.models import Product, Category, Brand,ProductVariant
from django.db.models import Q
from .models import Product
from django.http import JsonResponse


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
    variants = ProductVariant.objects.filter(
        product=product_id,
        stock__gt=0
    )

    related_product = Product.objects.filter(
        category=product_id.category,
        is_available=True
    ).exclude(
        id=product_id.id
    )[:10]

    context = {
        "data": product_id,
        "related_product": related_product,
        'variants':variants
    }

    return render(request, 'product-page.html', context)


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

def live_search(request):

    query = request.GET.get('q', '').strip()

    products = Product.objects.none()

    if query:

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(title_name__icontains=query) |
            Q(brand_name__name__icontains=query) |
            Q(category__name__icontains=query),
            is_available=True
        ).distinct()[:8]

    results = []

    for product in products:

        results.append({
            'name': product.name,
            'title': product.title_name,
            'price': str(product.price),
            'slug': product.slug,
        })

    return JsonResponse({
        'products': results
    })


from django.shortcuts import render
from django.db.models import Q
from .models import Product


def search_products(request):

    query = request.GET.get('q', '').strip()

    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(title_name__icontains=query) |
            Q(brand_name__name__icontains=query) |
            Q(category__name__icontains=query),
            is_available=True
        ).distinct()

    context = {
        'products': products,
        'query': query,
    }

    return render(
        request,
        'Products/search_results.html',
        context
    )