import random
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import CustomUser
from crm.models import Customer
from trips.models import Trip
from bookings.models import Booking

class Command(BaseCommand):
    help = 'Seeds the database with realistic sample data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding process...'))

        # Clean slate
        self.stdout.write('Deleting old data...')
        Payment.objects.all().delete()
        Booking.objects.all().delete()
        Trip.objects.all().delete()
        Customer.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        fake = Faker()

        # Create Users
        self.stdout.write('Creating users...')
        manager, _ = CustomUser.objects.get_or_create(username='manager', defaults={'role': 'manager', 'is_staff': True})
        manager.set_password('pass')
        manager.save()
        
        agent, _ = CustomUser.objects.get_or_create(username='agent', defaults={'role': 'agent'})
        agent.set_password('pass')
        agent.save()

        # Create Customers
        self.stdout.write('Creating customers...')
        customers = []
        for _ in range(15):
            customer = Customer.objects.create(
                full_name=fake.name(),
                phone_number=fake.unique.phone_number(),
                email=fake.unique.email(),
                passport_number=fake.unique.ssn().replace('-', ''),
                passport_expiry_date=fake.future_date(end_date='+5y'),
                nationality=fake.country(),
                date_of_birth=fake.date_of_birth(minimum_age=20, maximum_age=70)
            )
            customers.append(customer)

        # Create Trips
        self.stdout.write('Creating trips...')
        trips = []
        trip_names = [
            "Umrah Al-Noor (10 Days)", "Hajj VIP Package (20 Days)", "Ramadan Umrah Special",
            "Economy Umrah (7 Days)", "Spiritual Journey Package"
        ]
        statuses = ['scheduled', 'active', 'completed', 'cancelled']
        for name in trip_names:
            departure = fake.future_datetime(end_date='+60d')
            trip = Trip.objects.create(
                name=name,
                description=fake.paragraph(nb_sentences=3),
                departure_date=departure,
                return_date=departure + fake.time_delta(end_date='+15d'),
                total_seats=random.randint(20, 50),
                price_per_person=random.randrange(1500, 7000, 100),
                status=random.choice(statuses)
            )
            trips.append(trip)
        
        # Create Bookings
        self.stdout.write('Creating bookings...')
        active_trips = [t for t in trips if t.status in ['scheduled', 'active']]
        for _ in range(20):
            if not active_trips: continue
            trip = random.choice(active_trips)
            customer = random.choice(customers)
            # Ensure a customer is not booked twice on the same trip
            if Booking.objects.filter(customer=customer, trip=trip).exists():
                continue
            
            if trip.available_seats > 0:
                Booking.objects.create(
                    customer=customer,
                    trip=trip,
                    created_by=agent,
                    total_amount=trip.price_per_person,
                    status=random.choice([s[0] for s in Booking.STATUS_CHOICES if s[0] != 'cancelled'])
                )

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))