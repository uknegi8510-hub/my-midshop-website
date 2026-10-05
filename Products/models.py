from django.db import models
from autoslug import AutoSlugField
from  django_quill.fields import QuillField

class Category(models.Model):
    name = models.CharField(max_length=100 ,default='', null=True,blank=True)
    image=models.ImageField(upload_to='category/', default='category/default.png', blank=True, null=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=True,blank=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True,default='', null=True,blank=True)
    slug = AutoSlugField(populate_from='name', unique=True,null=True,blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',null=True,blank=True)
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50,default='', null=True,blank=True)
    title_name=models.CharField(max_length=400,default="",null=True,blank=True)
    slug = AutoSlugField(populate_from='name', unique=True,null=True,blank=True ,editable=True)
    General=QuillField(default="",blank=True,null=True)
    Product_details=QuillField(default="",blank=True,null=True)
    price = models.IntegerField(blank=True, null=True)
    discount_price = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name


class ProductVariant(models.Model):

    color = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    color_code = models.CharField(max_length=50, blank=True, null=True)

    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.color