import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Product, Deal
from orders.models import Order, OrderItem

class Command(BaseCommand):
    help = "Seed database with multi-day KFS orders for POS analytics and receipt testing."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding KFS Orders for POS & Analytics..."))

        Order.objects.all().delete()
        products = list(Product.objects.all())
        deals = list(Deal.objects.all())

        if not products and not deals:
            self.stdout.write(self.style.ERROR("No products or deals found! Run 'python manage.py seed_kfs' first."))
            return

        customer_names = [
            "Zain Malik", "Hamza Abbasi", "Usman Farooq", "Sana Ahmed", "Tariq Mahmood",
            "Bilal Khan", "Ayesha Siddiqui", "Omar Gul", "Fahad Mustafa", "Nida Yasir"
        ]

        order_types = ['Dine-in', 'Takeaway', 'Fast Delivery']
        payment_methods = ['Cash on Delivery', 'JazzCash/Easypaisa', 'Bank Transfer', 'Card']
        now = timezone.now()

        # Create orders over the past 14 days
        for day_offset in range(14, -1, -1):
            date_target = now - timedelta(days=day_offset)
            orders_today_count = random.randint(4, 9)

            for i in range(orders_today_count):
                order_time = date_target.replace(
                    hour=random.randint(12, 23),
                    minute=random.randint(0, 59)
                )

                cust_name = random.choice(customer_names)
                o_type = random.choice(order_types)
                p_method = random.choice(payment_methods)

                order = Order.objects.create(
                    customer_name=cust_name,
                    customer_phone="0344 2041131",
                    delivery_address="Main Commercial Street, Block B" if o_type == 'Fast Delivery' else "",
                    order_type=o_type,
                    payment_method=p_method,
                    status='Completed'
                )
                
                # Override created_at for historical analytics
                Order.objects.filter(id=order.id).update(created_at=order_time)

                # Add 1 to 4 items
                items_count = random.randint(1, 4)
                for _ in range(items_count):
                    if random.choice([True, False]) and products:
                        prod = random.choice(products)
                        qty = random.randint(1, 3)
                        OrderItem.objects.create(
                            order=order,
                            product=prod,
                            item_name=prod.name,
                            unit_price=prod.price,
                            quantity=qty
                        )
                    elif deals:
                        deal = random.choice(deals)
                        qty = random.randint(1, 2)
                        OrderItem.objects.create(
                            order=order,
                            deal=deal,
                            item_name=deal.title,
                            unit_price=deal.price,
                            quantity=qty
                        )

                order.refresh_from_db()
                order.recalculate_totals()

        self.stdout.write(self.style.SUCCESS(f"Successfully created {Order.objects.count()} POS orders across 14 days!"))
