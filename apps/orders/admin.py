from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'color', 'size', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Informations générales', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Livraison', {
            'fields': ('delivery_address', 'phone')
        }),
        ('Paiement', {
            'fields': ('total_amount', 'is_paid')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'estimated_delivery_date')
        }),
    )
