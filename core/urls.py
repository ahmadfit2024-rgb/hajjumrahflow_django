"""
URL configuration for HajjUmrahFlow project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    dashboard_view, 
    customer_list_view, 
    customer_add_view,
    trip_list_view,
    trip_detail_view,
    trip_add_view,
    trip_update_view,
)

urlpatterns = [
    # Main Dashboard
    path('', dashboard_view, name='dashboard'),
    
    # Customers
    path('customers/', customer_list_view, name='customer-list'),
    path('customers/add/', customer_add_view, name='customer-add'),
    
    # Trips
    path('trips/', trip_list_view, name='trip-list'),
    path('trips/add/', trip_add_view, name='trip-add'),
    path('trips/<int:pk>/', trip_detail_view, name='trip-detail'),
    path('trips/<int:pk>/update/', trip_update_view, name='trip-update'),

    # Admin and API routes
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('crm.urls')),
    path('api/v1/', include('trips.urls')),
    path('api/v1/', include('bookings.urls')),
]