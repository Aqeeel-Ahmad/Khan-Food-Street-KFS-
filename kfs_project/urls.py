from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders.views import sales_analytics_view, export_sales_csv_view

urlpatterns = [
    path('admin/sales-analytics/', sales_analytics_view, name='sales_analytics'),
    path('admin/sales-analytics/export/', export_sales_csv_view, name='export_sales_csv'),
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
