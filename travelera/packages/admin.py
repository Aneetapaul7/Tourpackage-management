


from django.contrib import admin
from .models import Package, PackageImage

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ('package', 'caption', 'created_at')
    list_filter = ('package', 'created_at')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'destination', 'price', 'status', 'is_active', 'expiry_date')
    list_filter = ('status', 'destination', 'vendor')
    search_fields = ('title', 'description', 'destination')
    actions = ['approve_packages', 'reject_packages']

    def approve_packages(self, request, queryset):
        queryset.update(status=Package.APPROVED)

    approve_packages.short_description = "Approve selected packages"

    def reject_packages(self, request, queryset):
        queryset.update(status=Package.REJECTED)

    reject_packages.short_description = "Reject selected packages"

    def is_active(self, obj):
        return obj.is_active

    is_active.boolean = True
    is_active.short_description = 'Active'