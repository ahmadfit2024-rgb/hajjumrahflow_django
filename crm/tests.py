from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser
from crm.models import Customer


class CustomerPermissionsTests(APITestCase):
    def setUp(self):
        self.manager = CustomUser.objects.create_user(username='manager', password='pass', role='manager')
        self.agent = CustomUser.objects.create_user(username='agent', password='pass', role='agent')
        self.accountant = CustomUser.objects.create_user(username='accountant', password='pass', role='accountant')
        self.customer_data = {
            'full_name': 'Test User',
            'phone_number': '+1000000000',
            'email': 'user@example.com',
            'passport_number': 'P123456',
            'passport_expiry_date': '2030-01-01',
            'nationality': 'Test',
            'date_of_birth': '1990-01-01'
        }

    def test_agent_can_create_customer(self):
        self.client.force_authenticate(self.agent)
        response = self.client.post('/api/v1/customers/', self.customer_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_accountant_cannot_create_customer(self):
        self.client.force_authenticate(self.accountant)
        response = self.client.post('/api/v1/customers/', self.customer_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_agent_can_upload_document(self):
        customer = Customer.objects.create(
            full_name='Doc Cust', phone_number='+1999999999', passport_number='DOC1',
            passport_expiry_date='2030-01-01', nationality='Test', date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(self.agent)
        payload = {
            'customer': customer.id,
            'document_type': 'passport_copy',
            'file': SimpleUploadedFile('doc.jpg', b'filecontent', content_type='image/jpeg')
        }
        response = self.client.post('/api/v1/documents/', payload, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'uploaded')

    def test_accountant_cannot_upload_document(self):
        customer = Customer.objects.create(
            full_name='Doc Cust2', phone_number='+1888888888', passport_number='DOC2',
            passport_expiry_date='2030-01-01', nationality='Test', date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(self.accountant)
        payload = {
            'customer': customer.id,
            'document_type': 'passport_copy',
            'file': SimpleUploadedFile('doc.jpg', b'filecontent', content_type='image/jpeg')
        }
        response = self.client.post('/api/v1/documents/', payload, format='multipart')
        self.assertEqual(response.status_code, 403)