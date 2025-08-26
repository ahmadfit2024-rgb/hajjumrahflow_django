from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from crm.models import Customer
from trips.models import Trip
from bookings.models import Booking
from crm.forms import CustomerForm # <-- استيراد النموذج الجديد

@login_required
def dashboard_view(request):
    """
    يعرض لوحة التحكم الرئيسية ببيانات حقيقية من قاعدة البيانات.
    """
    total_customers = Customer.objects.count()
    active_trips = Trip.objects.filter(status='active').count()
    pending_bookings = Booking.objects.filter(status__in=['payment_pending', 'documents_pending']).count()
    
    context = {
        'total_customers': total_customers,
        'active_trips': active_trips,
        'pending_bookings': pending_bookings,
    }
    return render(request, 'dashboard.html', context)

@login_required
def customer_list_view(request):
    """
    يعرض قائمة بجميع العملاء المسجلين في النظام.
    """
    customers = Customer.objects.all().order_by('-created_at')
    context = {
        'customers': customers
    }
    return render(request, 'crm/customer_list.html', context)

@login_required
def customer_add_view(request):
    """
    يعالج عرض وحفظ نموذج إضافة عميل جديد.
    """
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-list') # توجيه المستخدم لقائمة العملاء بعد الحفظ
    else:
        form = CustomerForm()
        
    context = {
        'form': form
    }
    return render(request, 'crm/customer_form.html', context)