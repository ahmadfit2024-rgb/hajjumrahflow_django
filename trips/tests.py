from rest_framework.test import APITestCase
from users.models import CustomUser
from trips.models import Trip
from crm.models import Customer
from bookings.models import Booking


class TripManifestTests(APITestCase):
    def setUp(self):
        self.manager = CustomUser.objects.create_user(username='manager', password='pass', role='manager')
        self.trip = Trip.objects.create(
            name='Test Trip',
            departure_date='2030-01-01T00:00:00Z',
            return_date='2030-01-10T00:00:00Z',
            total_seats=5,
            price_per_person=1000
        )
        self.customer1 = Customer.objects.create(
            full_name='Cust One',
            phone_number='+1111111111',
            passport_number='P1',
            passport_expiry_date='2030-01-01',
            nationality='Test',
            date_of_birth='1990-01-01'
        )
        self.customer2 = Customer.objects.create(
            full_name='Cust Two',
            phone_number='+2222222222',
            passport_number='P2',
            passport_expiry_date='2030-01-01',
            nationality='Test',
            date_of_birth='1990-01-01'
        )
        Booking.objects.create(customer=self.customer1, trip=self.trip)
        Booking.objects.create(customer=self.customer2, trip=self.trip, status='cancelled')

    def test_manifest_lists_active_bookings(self):
        self.client.force_authenticate(self.manager)
        url = f'/api/v1/trips/{self.trip.id}/manifest/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['full_name'], 'Cust One')