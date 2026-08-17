import csv
from decimal import Decimal
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, Q
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from core.models import Product, Deal, Category
from .models import Order, OrderItem

def order_receipt_view(request, order_id):
    """Render a clean 80mm / A4 printable thermal POS receipt."""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'items': order.items.all(),
        'cashier_name': request.user.username if request.user.is_authenticated else 'KFS Cashier',
    }
    return render(request, 'orders/receipt.html', context)


def batch_order_receipt_view(request):
    """Render printable receipts for multiple order IDs."""
    raw_ids = request.GET.get('ids', '')
    if raw_ids:
        order_ids = [int(i) for i in raw_ids.split(',') if i.isdigit()]
        orders = Order.objects.filter(id__in=order_ids)
    else:
        orders = []
    
    context = {
        'orders': orders,
        'cashier_name': request.user.username if request.user.is_authenticated else 'KFS Staff',
    }
    return render(request, 'orders/batch_receipt.html', context)


def track_order_view(request, order_number=None):
    """Public Order Tracking view allowing customers to track order status by invoice number or phone."""
    query = request.GET.get('q', '').strip() or order_number
    orders = []
    searched = False
    searched_query = query

    if query:
        searched = True
        orders = Order.objects.filter(
            Q(order_number__icontains=query) | Q(customer_phone__icontains=query)
        ).order_by('-created_at')[:10]

    context = {
        'orders': orders,
        'searched': searched,
        'searched_query': searched_query,
    }
    return render(request, 'orders/track_order.html', context)


@staff_member_required
def pos_checkout_view(request):
    """POS Terminal checkout view for restaurant staff."""
    products = Product.objects.filter(is_available=True)
    deals = Deal.objects.filter(is_active=True)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', 'Walk-in Customer')
        customer_phone = request.POST.get('customer_phone', '0344 2041131')
        order_type = request.POST.get('order_type', 'Dine-in')
        payment_method = request.POST.get('payment_method', 'Cash on Delivery')
        delivery_address = request.POST.get('delivery_address', '')
        
        try:
            discount = Decimal(request.POST.get('discount', '0.00') or '0.00')
        except:
            discount = Decimal('0.00')

        try:
            tax = Decimal(request.POST.get('tax', '0.00') or '0.00')
        except:
            tax = Decimal('0.00')

        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            order_type=order_type,
            payment_method=payment_method,
            delivery_address=delivery_address,
            discount=discount,
            tax=tax,
            status='Completed'
        )

        # Parse selected items
        item_keys = [k for k in request.POST.keys() if k.startswith('qty_prod_') or k.startswith('qty_deal_')]
        for key in item_keys:
            try:
                qty = int(request.POST.get(key, 0))
                if qty <= 0:
                    continue
                if key.startswith('qty_prod_'):
                    prod_id = int(key.replace('qty_prod_', ''))
                    product = Product.objects.get(id=prod_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        item_name=product.name,
                        unit_price=product.price,
                        quantity=qty
                    )
                elif key.startswith('qty_deal_'):
                    deal_id = int(key.replace('qty_deal_', ''))
                    deal = Deal.objects.get(id=deal_id)
                    OrderItem.objects.create(
                        order=order,
                        deal=deal,
                        item_name=deal.title,
                        unit_price=deal.price,
                        quantity=qty
                    )
            except Exception as e:
                continue

        order.recalculate_totals()
        messages.success(request, f"Order {order.order_number} created successfully!")
        
        if 'print_now' in request.POST:
            return redirect('order_receipt', order_id=order.id)
        return redirect('pos_checkout')

    context = {
        'products': products,
        'deals': deals,
    }
    return render(request, 'orders/pos_checkout.html', context)


@staff_member_required
def sales_analytics_view(request):
    """Staff & Admin Sales Analytics Dashboard (Daily, Weekly, Monthly reports)."""
    selected_date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = timezone.now().date()

    # 1. DAILY REPORT
    today_orders = Order.objects.filter(created_at__date=selected_date, status='Completed')
    today_revenue = today_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    today_order_count = today_orders.count()

    today_item_sales = OrderItem.objects.filter(order__in=today_orders) \
        .values('item_name') \
        .annotate(
            total_qty=Sum('quantity'),
            total_volume=Sum(F('unit_price') * F('quantity'), output_field=DecimalField())
        ) \
        .order_by('-total_qty')

    # 2. WEEKLY REPORT (Last 7 Days)
    seven_days_ago = selected_date - timedelta(days=6)
    weekly_orders = Order.objects.filter(created_at__date__gte=seven_days_ago, created_at__date__lte=selected_date, status='Completed')
    weekly_revenue = weekly_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    weekly_count = weekly_orders.count()

    # Day-by-day comparison chart
    weekly_chart_data = Order.objects.filter(created_at__date__gte=seven_days_ago, created_at__date__lte=selected_date, status='Completed') \
        .annotate(day=TruncDay('created_at')) \
        .values('day') \
        .annotate(daily_total=Sum('total_amount'), order_count=Count('id')) \
        .order_by('day')

    weekly_top_items = OrderItem.objects.filter(order__in=weekly_orders) \
        .values('item_name') \
        .annotate(
            total_qty=Sum('quantity'),
            total_volume=Sum(F('unit_price') * F('quantity'), output_field=DecimalField())
        ) \
        .order_by('-total_qty')[:5]

    # 3. MONTHLY REPORT
    first_day_curr_month = selected_date.replace(day=1)
    prev_month_last_day = first_day_curr_month - timedelta(days=1)
    first_day_prev_month = prev_month_last_day.replace(day=1)

    curr_month_orders = Order.objects.filter(created_at__date__gte=first_day_curr_month, created_at__date__lte=selected_date, status='Completed')
    curr_month_revenue = curr_month_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    curr_month_count = curr_month_orders.count()

    prev_month_orders = Order.objects.filter(created_at__date__gte=first_day_prev_month, created_at__date__lte=prev_month_last_day, status='Completed')
    prev_month_revenue = prev_month_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

    # Monthly Sales by Category
    category_breakdown = OrderItem.objects.filter(order__in=curr_month_orders, product__isnull=False) \
        .values('product__category__name') \
        .annotate(
            total_qty=Sum('quantity'),
            total_sales=Sum(F('unit_price') * F('quantity'), output_field=DecimalField())
        ) \
        .order_by('-total_sales')

    context = {
        'selected_date': selected_date_str,
        'today_revenue': today_revenue,
        'today_order_count': today_order_count,
        'today_item_sales': today_item_sales,
        
        'weekly_revenue': weekly_revenue,
        'weekly_count': weekly_count,
        'weekly_chart_data': list(weekly_chart_data),
        'weekly_top_items': weekly_top_items,
        
        'curr_month_revenue': curr_month_revenue,
        'curr_month_count': curr_month_count,
        'prev_month_revenue': prev_month_revenue,
        'category_breakdown': category_breakdown,
    }
    return render(request, 'orders/sales_analytics.html', context)


@staff_member_required
def export_sales_csv_view(request):
    """Export Sales Analytics as CSV file."""
    response = HttpResponse(content_type='text/csv')
    filename = f"KFS_Sales_Report_{timezone.now().strftime('%Y%m%d')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Order Number', 'Date', 'Customer Name', 'Phone', 'Order Type', 'Payment Method', 'Status', 'Total Amount (Rs)'])

    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        writer.writerow([
            order.order_number,
            order.created_at.strftime('%Y-%m-%d %H:%M'),
            order.customer_name,
            order.customer_phone,
            order.order_type,
            order.payment_method,
            order.status,
            order.total_amount
        ])

    return response
