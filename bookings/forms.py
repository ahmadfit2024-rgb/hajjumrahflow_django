from django import forms
from .models import Booking, Customer, Trip

class BookingForm(forms.ModelForm):
    # نستخدم حقول خاصة لجلب قائمة العملاء والرحلات
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by('full_name'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    trip = forms.ModelChoiceField(
        queryset=Trip.objects.filter(status__in=['scheduled', 'active']).order_by('name'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['customer', 'trip', 'total_amount', 'status']
        widgets = {
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }