from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trip
from .serializers import TripSerializer
from users.permissions import RolePermission
from bookings.models import Booking
from crm.serializers import CustomerSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().order_by('departure_date')
    serializer_class = TripSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            roles = ['manager']
        else:
            roles = ['manager', 'agent', 'accountant']
        return [RolePermission(roles)]

    @action(detail=True, methods=['get'])
    def manifest(self, request, pk=None):
        trip = self.get_object()
        bookings = Booking.objects.filter(trip=trip).exclude(status='cancelled').select_related('customer')
        data = [CustomerSerializer(b.customer).data for b in bookings]
        return Response(data)