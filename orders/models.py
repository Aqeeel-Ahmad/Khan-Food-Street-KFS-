from decimal import Decimal
from django.db import models
from django.utils import timezone
from core.models import Product, Deal
import uuid

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('Dine-in', 'Dine-in'),
        ('Takeaway', 'Takeaway'),
        ('Fast Delivery', 'Fast Delivery'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash on Delivery', 'Cash on Delivery / Cash'),
        ('JazzCash/Easypaisa', 'JazzCash / Easypaisa'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Card', 'Debit / Credit Card'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    customer_name = models.CharField(max_length=100, default="Walk-in Customer")
    customer_phone = models.CharField(max_length=30, blank=True, null=True, default="0344 2041131")
    delivery_address = models.TextField(blank=True, null=True, help_text="Required for Fast Delivery orders")
    order_type = models.CharField(max_length=30, choices=ORDER_TYPE_CHOICES, default='Dine-in')
    payment_method = models.CharField(max_length=40, choices=PAYMENT_METHOD_CHOICES, default='Cash on Delivery')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text="Sales tax / GST if applicable")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "POS Order"
        verbose_name_plural = "POS Orders"

    def save(self, *args, **kwargs):
        if not self.order_number:
            date_str = timezone.now().strftime("%Y%m%d")
            short_id = str(uuid.uuid4().hex[:4]).upper()
            self.order_number = f"KFS-{date_str}-{short_id}"
        super().save(*args, **kwargs)

    def recalculate_totals(self):
        items = self.items.all()
        calculated_subtotal = sum((item.line_total for item in items), Decimal('0.00'))
        self.subtotal = Decimal(str(calculated_subtotal))
        discount_val = Decimal(str(self.discount or '0.00'))
        tax_val = Decimal(str(self.tax or '0.00'))
        total_val = (self.subtotal - discount_val) + tax_val
        self.total_amount = max(Decimal('0.00'), total_val)
        self.save(update_fields=['subtotal', 'total_amount'])

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} (Rs {self.total_amount})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        return Decimal(str(self.unit_price)) * Decimal(str(self.quantity))

    def save(self, *args, **kwargs):
        if not self.item_name:
            if self.product:
                self.item_name = self.product.name
            elif self.deal:
                self.item_name = self.deal.title
        super().save(*args, **kwargs)
        if self.order_id:
            self.order.recalculate_totals()

    def __str__(self):
        return f"{self.quantity}x {self.item_name} @ Rs {self.unit_price}"
