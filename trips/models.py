from django.db import models


class Trip(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    departure_date = models.DateTimeField()
    return_date = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled',
    )

    def __str__(self):
        return self.name

    @property
    def booked_seats(self):
        return self.bookings.exclude(status='cancelled').count()

    @property
    def available_seats(self):
        return self.total_seats - self.booked_seats