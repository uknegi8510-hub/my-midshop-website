from django.contrib import admin
from  Products.models import Category,Product,ProductImage,Brand,ProductVariant

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','is_active','created_at')
class ProductImageInline(admin.TabularInline):
    model=ProductImage
    extra=1
class ProductVariantInline(admin.TabularInline):
    model=ProductVariant
    extra=1
class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageInline,ProductVariantInline]
    list_display=('name','price','is_available','created_at')
    fields=(
        'category',
        'brand_name',
        'name',
        'title_name',
        'General',
        'Product_details',
        'price',
        "discount_price",
        'stock',
        'is_available',

    )
class BrandAdmin(admin.ModelAdmin):
    list_display=('logo','name','is_active')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Brand,BrandAdmin)

