from rest_framework import viewsets, filters
from .models import Customer, Document, CommunicationLog
from .serializers import CustomerSerializer, DocumentSerializer, CommunicationLogSerializer
from users.permissions import RolePermission


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'phone_number', 'email', 'passport_number']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            roles = ['manager', 'agent']
        elif self.action == 'destroy':
            roles = ['manager']
        else:
            roles = ['manager', 'agent', 'accountant']
        return [RolePermission(roles)]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            roles = ['manager', 'agent']
        elif self.action == 'destroy':
            roles = ['manager']
        else:
            roles = ['manager', 'agent', 'accountant']
        return [RolePermission(roles)]


class CommunicationLogViewSet(viewsets.ModelViewSet):
    queryset = CommunicationLog.objects.all().order_by('-created_at')
    serializer_class = CommunicationLogSerializer

    def get_permissions(self):
        roles = ['manager', 'agent', 'accountant']
        return [RolePermission(roles)]