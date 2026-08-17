from django.urls import path
from . import views

urlpatterns = [
    path('track/', views.track_order_view, name='track_order'),
    path('receipt/<int:order_id>/', views.order_receipt_view, name='order_receipt'),
    path('receipt/batch/', views.batch_order_receipt_view, name='batch_order_receipt'),
    path('pos/', views.pos_checkout_view, name='pos_checkout'),
    path('admin/sales-analytics/', views.sales_analytics_view, name='sales_analytics'),
    path('admin/sales-analytics/export/', views.export_sales_csv_view, name='export_sales_csv'),
]
