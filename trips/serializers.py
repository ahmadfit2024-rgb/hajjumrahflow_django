from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    booked_seats = serializers.IntegerField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'