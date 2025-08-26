"""
URL configuration for HajjUmrahFlow project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    dashboard_view, 
    customer_list_view, customer_add_view, customer_update_view, customer_detail_view,
    trip_list_view, trip_detail_view, trip_add_view, trip_update_view,
    booking_list_view, booking_add_view, booking_detail_view,
)

urlpatterns = [
    # Main Dashboard
    path('', dashboard_view, name='web_dashboard'),
    
    # Customers
    path('customers/', customer_list_view, name='web_customer_list'),
    path('customers/add/', customer_add_view, name='web_customer_add'),
    path('customers/<int:pk>/', customer_detail_view, name='web_customer_detail'),
    path('customers/<int:pk>/update/', customer_update_view, name='web_customer_update'),
    
    # Trips
    path('trips/', trip_list_view, name='web_trip_list'),
    path('trips/add/', trip_add_view, name='web_trip_add'),
    path('trips/<int:pk>/', trip_detail_view, name='web_trip_detail'),
    path('trips/<int:pk>/update/', trip_update_view, name='web_trip_update'),

    # Bookings
    path('bookings/', booking_list_view, name='web_booking_list'),
    path('bookings/add/', booking_add_view, name='web_booking_add'),
    path('bookings/<int:pk>/', booking_detail_view, name='web_booking_detail'),

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