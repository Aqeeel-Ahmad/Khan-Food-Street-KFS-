from django.contrib import admin
from django.utils.html import mark_safe
from django.urls import reverse
from django.shortcuts import redirect
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'deal', 'item_name', 'unit_price', 'quantity', 'get_line_total')
    readonly_fields = ('get_line_total',)

    def get_line_total(self, obj):
        if obj.id:
            return f"Rs {obj.line_total:.2f}"
        return "Rs 0.00"
    get_line_total.short_description = "Line Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'order_type', 'payment_method', 'total_amount', 'status', 'created_at', 'receipt_button')
    list_filter = ('status', 'order_type', 'payment_method', ('created_at', admin.DateFieldListFilter))
    search_fields = ('order_number', 'customer_name', 'customer_phone')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    actions = ['batch_print_receipts', 'mark_as_completed']
    list_per_page = 20

    def receipt_button(self, obj):
        url = reverse('order_receipt', args=[obj.id])
        return mark_safe(f'<a href="{url}" target="_blank" style="background-color: #F5A623; color: #121212; font-weight: bold; padding: 4px 10px; border-radius: 6px; text-decoration: none; font-size: 11px;">🖨️ Print Receipt</a>')
    receipt_button.short_description = 'Thermal Receipt'

    @admin.action(description="🖨️ Batch Print Selected Thermal Receipts")
    def batch_print_receipts(self, request, queryset):
        order_ids = ",".join(str(o.id) for o in queryset)
        url = reverse('batch_order_receipt') + f"?ids={order_ids}"
        return redirect(url)

    @admin.action(description="✅ Mark selected orders as Completed")
    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
        self.message_user(request, f"Updated {queryset.count()} orders to Completed.")
