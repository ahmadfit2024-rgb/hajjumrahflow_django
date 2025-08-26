from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'name', 'description', 'departure_date', 'return_date',
            'total_seats', 'price_per_person', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'departure_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'return_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }