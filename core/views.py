from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from crm.models import Customer
from trips.models import Trip
from bookings.models import Booking
from crm.forms import CustomerForm
from trips.forms import TripForm
from bookings.forms import BookingForm # <-- استيراد نموذج الحجوزات

@login_required
def dashboard_view(request):
    total_customers = Customer.objects.count()
    active_trips = Trip.objects.filter(status='active').count()
    pending_bookings = Booking.objects.filter(status__in=['payment_pending', 'documents_pending']).count()
    
    context = {
        'total_customers': total_customers,
        'active_trips': active_trips,
        'pending_bookings': pending_bookings,
    }
    return render(request, 'dashboard.html', context)

# --- Customer Views ---
@login_required
def customer_list_view(request):
    customers = Customer.objects.all().order_by('-created_at')
    context = { 'customers': customers }
    return render(request, 'crm/customer_list.html', context)

@login_required
def customer_add_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer has been added successfully.')
            return redirect('customer-list')
    else:
        form = CustomerForm()
    context = { 'form': form }
    return render(request, 'crm/customer_form.html', context)

# --- Trip Views ---
@login_required
def trip_list_view(request):
    trips = Trip.objects.all().order_by('-departure_date')
    context = { 'trips': trips }
    return render(request, 'trips/trip_list.html', context)

@login_required
def trip_detail_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    context = { 'trip': trip }
    return render(request, 'trips/trip_detail.html', context)

@login_required
def trip_add_view(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip has been created successfully.')
            return redirect('trip-list')
    else:
        form = TripForm()
    context = { 'form': form, 'form_title': 'Add New Trip' }
    return render(request, 'trips/trip_form.html', context)

@login_required
def trip_update_view(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, f'Trip "{trip.name}" has been updated successfully.')
            return redirect('trip-detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)
    context = { 'form': form, 'form_title': f'Update: {trip.name}' }
    return render(request, 'trips/trip_form.html', context)

# --- Booking Views (NEW & IMPROVED) ---
@login_required
def booking_list_view(request):
    """ يعرض قائمة بجميع الحجوزات. """
    bookings = Booking.objects.select_related('customer', 'trip').all().order_by('-booking_date')
    context = { 'bookings': bookings }
    return render(request, 'bookings/booking_list.html', context)

@login_required
def booking_add_view(request):
    """ يعالج عرض وحفظ نموذج إضافة حجز جديد. """
    form = BookingForm(request.POST or None)
    
    # Check if coming from a specific trip page
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
                return redirect('booking-list')
            else:
                messages.error(request, 'This trip has no available seats.')
        
    context = {
        'form': form,
        'form_title': 'Create New Booking'
    }
    return render(request, 'bookings/booking_form.html', context)