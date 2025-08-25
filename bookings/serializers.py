from rest_framework import serializers
from .models import Booking, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['booking', 'recorded_by', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'