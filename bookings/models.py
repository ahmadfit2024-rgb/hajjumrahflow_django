from django.db import models
from django.conf import settings
from crm.models import Customer
from trips.models import Trip


class Booking(models.Model):
    STATUS_CHOICES = [
        ('documents_pending', 'Documents Pending'),
        ('payment_pending', 'Payment Pending'),
        ('confirmed', 'Confirmed'),
        ('paid_fully', 'Paid Fully'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='documents_pending')
    last_reminder_sent_at = models.DateTimeField(blank=True, null=True)


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'), ('online', 'Online')])
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)