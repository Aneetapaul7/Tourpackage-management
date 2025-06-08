from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Vendor, Customer


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'user_type')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'user_type')}),
    )


class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user_info')

    def user_info(self, obj):
        return f"{obj.user.get_full_name()} ({obj.user.phone_number})"

    user_info.short_description = 'User Info'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'phone_number')

    def user_info(self, obj):
        return obj.user.get_full_name()

    user_info.short_description = 'Name'

    def phone_number(self, obj):
        return obj.user.phone_number

    phone_number.short_description = 'Phone Number'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Customer, CustomerAdmin)