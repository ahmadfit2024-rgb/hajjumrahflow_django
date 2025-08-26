"""
URL configuration for HajjUmrahFlow project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# استيراد كل الدوال مرة واحدة
from .views import dashboard_view, customer_list_view, customer_add_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('customers/', customer_list_view, name='customer-list'),
    path('customers/add/', customer_add_view, name='customer-add'), # <-- رابط صفحة الإضافة

    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('crm.urls')),
    path('api/v1/', include('trips.urls')),
    path('api/v1/', include('bookings.urls')),
]