from rest_framework.test import APITestCase
from users.models import CustomUser
from crm.models import Customer
from trips.models import Trip
from .models import Booking
from datetime import date, timedelta
from django.utils import timezone


class BookingAvailabilityTests(APITestCase):
    def setUp(self):
        self.agent = CustomUser.objects.create_user(username='agent', password='pass', role='agent')
        self.customer1 = Customer.objects.create(
            full_name='Cust One', phone_number='+1000000001', passport_number='P1',
            passport_expiry_date=date(2030, 1, 1), nationality='X', date_of_birth=date(1990, 1, 1)
        )
        self.customer2 = Customer.objects.create(
            full_name='Cust Two', phone_number='+1000000002', passport_number='P2',
            passport_expiry_date=date(2030, 1, 1), nationality='X', date_of_birth=date(1990, 1, 1)
        )
        now = timezone.now()
        self.trip = Trip.objects.create(
            name='Test Trip', departure_date=now, return_date=now + timedelta(days=7),
            total_seats=1, price_per_person=100
        )

    def test_prevent_overbooking(self):
        self.client.force_authenticate(self.agent)
        res1 = self.client.post('/api/v1/bookings/', {'customer': self.customer1.id, 'trip': self.trip.id, 'total_amount': 100}, format='json')
        self.assertEqual(res1.status_code, 201)
        res2 = self.client.post('/api/v1/bookings/', {'customer': self.customer2.id, 'trip': self.trip.id, 'total_amount': 100}, format='json')
        self.assertEqual(res2.status_code, 400)


class PaymentStatusTests(APITestCase):
    def setUp(self):
        self.manager = CustomUser.objects.create_user(username='manager', password='pass', role='manager')
        self.accountant = CustomUser.objects.create_user(username='accountant', password='pass', role='accountant')
        self.customer = Customer.objects.create(
            full_name='Cust', phone_number='+2000000000', passport_number='P3',
            passport_expiry_date=date(2030, 1, 1), nationality='X', date_of_birth=date(1990, 1, 1)
        )
        now = timezone.now()
        self.trip = Trip.objects.create(
            name='Trip', departure_date=now, return_date=now + timedelta(days=7),
            total_seats=5, price_per_person=100
        )
        self.booking = Booking.objects.create(customer=self.customer, trip=self.trip, total_amount=100, status='payment_pending', created_by=self.manager)

    def test_payment_updates_status(self):
        self.client.force_authenticate(self.accountant)
        url = f'/api/v1/bookings/{self.booking.id}/add_payment/'
        res1 = self.client.post(url, {'amount_paid': 60, 'payment_date': '2025-01-01', 'payment_method': 'cash'}, format='json')
        self.assertEqual(res1.status_code, 201)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'confirmed')
        res2 = self.client.post(url, {'amount_paid': 40, 'payment_date': '2025-01-02', 'payment_method': 'cash'}, format='json')
        self.assertEqual(res2.status_code, 201)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'paid_fully')