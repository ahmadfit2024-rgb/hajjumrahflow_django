from rest_framework import viewsets, decorators, response, status, exceptions
from .models import Booking, Payment
from .serializers import BookingSerializer, PaymentSerializer
from users.permissions import RolePermission


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-booking_date')
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            roles = ['manager', 'agent']
        elif self.action in ['destroy']:
            roles = ['manager']
        elif self.action in ['add_payment']:
            roles = ['manager', 'agent', 'accountant']
        elif self.action in ['cancel']:
            roles = ['manager', 'agent']
        else:
            roles = ['manager', 'agent', 'accountant']
        return [RolePermission(roles)]

    def perform_create(self, serializer):
        trip = serializer.validated_data['trip']
        if trip.available_seats <= 0:
            raise exceptions.ValidationError('No seats available for this trip.')
        serializer.save(created_by=self.request.user)

    @decorators.action(detail=True, methods=['post'])
    def add_payment(self, request, pk=None):
        booking = self.get_object()
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(booking=booking, recorded_by=request.user)
        total_paid = sum(p.amount_paid for p in booking.payments.all())
        if total_paid >= booking.total_amount:
            booking.status = 'paid_fully'
        else:
            booking.status = 'confirmed'
        booking.save(update_fields=['status'])
        return response.Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'cancelled'
        booking.save(update_fields=['status'])
        return response.Response({'status': 'cancelled'})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action in ['create']:
            roles = ['manager', 'agent', 'accountant']
        elif self.action in ['update', 'partial_update', 'destroy']:
            roles = ['manager', 'accountant']
        else:
            roles = ['manager', 'agent', 'accountant']
        return [RolePermission(roles)]