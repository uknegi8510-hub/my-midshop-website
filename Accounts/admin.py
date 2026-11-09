from django.contrib import admin
from Accounts.models import User, UserProfile, Address


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    fields = (
        'full_name',
        'phone',
        'address_line',
        'city',
        'state',
        'pincode',
        'country',
        'address_type',
        'is_default',
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'email',
        'is_verified',
        'is_superuser',
        'is_staff',
    )

    search_fields = (
        'display_name',
        'email',
    )

    inlines = [AddressInline]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'profile_image',
        'gender',
        'date_of_birth',
        'created_at',
    )

    search_fields = (
        'user__display_name',
        'user__email',
    )

    list_filter = (
        'gender',
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)