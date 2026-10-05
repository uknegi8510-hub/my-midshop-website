from django.contrib import admin
from Accounts.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('display_name','email','is_verified','is_superuser','is_staff')

admin.site.register(User,UserAdmin)
