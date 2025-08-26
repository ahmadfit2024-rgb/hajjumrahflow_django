from django.db import models
from django.conf import settings


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    passport_number = models.CharField(max_length=50, unique=True)
    passport_expiry_date = models.DateField()
    nationality = models.CharField(max_length=100, default='')
    date_of_birth = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Document(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=[('passport_copy', 'Passport Copy'), ('personal_photo', 'Personal Photo'), ('other', 'Other')])
    status = models.CharField(max_length=20, choices=[('required', 'Required'), ('uploaded', 'Uploaded'), ('verified', 'Verified')], default='uploaded')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CommunicationLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='communications')
    channel = models.CharField(max_length=20, choices=[('email', 'Email'), ('whatsapp', 'WhatsApp'), ('sms', 'SMS')])
    direction = models.CharField(max_length=10, default='outgoing')
    content = models.TextField()
    status = models.CharField(max_length=20, default='sent')
    triggered_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)