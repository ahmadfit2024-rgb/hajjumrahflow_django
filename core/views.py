from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from crm.models import Customer
from trips.models import Trip
from bookings.models import Booking
from crm.forms import CustomerForm
from trips.forms import TripForm
from bookings.forms import BookingForm

@login_required
def dashboard_view(request):
    total_customers = Customer.objects.count()
    active_trips = Trip.objects.filter(status='active').count()
    pending_bookings = Booking.objects.filter(status__in=['payment_pending', 'documents_pending']).count()
    
    context = {
        'total_customers': total_customers, 'active_trips': active_trips, 'pending_bookings': pending_bookings,
    }
    return render(request, 'dashboard.html', context)

# --- Customer Views ---
@login_required
def customer_list_view(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'crm/customer_list.html', {'customers': customers})

@login_required
def customer_detail_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'crm/customer_detail.html', {'customer': customer})

@login_required
def customer_add_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer has been added successfully.')
            return redirect('web_customer_list')
    else:
        form = CustomerForm()
    return render(request, 'crm/customer_form.html', {'form': form, 'form_title': 'Add New Customer'})

@login_required
def customer_update_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer "{customer.full_name}" has been updated successfully.')
            return redirect('web_customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_form.html', {'form': form, 'form_title': f'Update: {customer.full_name}'})


# --- Trip Views ---
@login_required
def trip_list_view(request):
    trips = Trip.objects.all().order_by('-departure_date')
    return render(request, 'trips/trip_list.html', {'trips': trips})

@login_required
def trip_detail_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'trips/trip_detail.html', {'trip': trip})

@login_required
def trip_add_view(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip has been created successfully.')
            return redirect('web_trip_list')
    else:
        form = TripForm()
    return render(request, 'trips/trip_form.html', {'form': form, 'form_title': 'Add New Trip'})

@login_required
def trip_update_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, f'Trip "{trip.name}" has been updated successfully.')
            return redirect('web_trip_detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)
    return render(request, 'trips/trip_form.html', {'form': form, 'form_title': f'Update: {trip.name}'})

# --- Booking Views ---
@login_required
def booking_list_view(request):
    bookings = Booking.objects.select_related('customer', 'trip').all().order_by('-booking_date')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('customer', 'trip'), pk=pk)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def booking_add_view(request):
    form = BookingForm(request.POST or None)
    trip_id = request.GET.get('trip_id')
    if trip_id:
        form.fields['trip'].initial = trip_id

    if request.method == 'POST':
        if form.is_valid():
            trip = form.cleaned_data['trip']
            if trip.available_seats > 0:
                booking = form.save(commit=False)
                booking.created_by = request.user
                booking.save()
                messages.success(request, 'Booking has been created successfully.')
                return redirect('web_booking_list')
            else:
                messages.error(request, 'This trip has no available seats.')
    
    return render(request, 'bookings/booking_form.html', {'form': form, 'form_title': 'Create New Booking'})