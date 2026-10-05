from django.contrib import admin
from Wishlist.models import Wishlist

# Register your models here.
class WishlistAdmin(admin.ModelAdmin):
    list_display=('user','product','created_at')

admin.site.register(Wishlist,WishlistAdmin)


