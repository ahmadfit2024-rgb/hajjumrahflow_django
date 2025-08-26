from rest_framework.routers import DefaultRouter

# Namespacing for URL reversal in templates
app_name = 'crm'
from .views import CustomerViewSet, DocumentViewSet, CommunicationLogViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'communication-logs', CommunicationLogViewSet, basename='communicationlog')
urlpatterns = router.urls