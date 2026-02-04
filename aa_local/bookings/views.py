from django.shortcuts import render, redirect, get_object_or_404
from services.models import Service 
from accounts.models import Address
from .models import Booking
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.contrib import messages


# Create your views here.
def booking(request):
    return render(request,'customer/bookings/my_bookings.html')

def booking_detail(request):
    return render(request,'customer/bookings/booking_detail.html')

@login_required
def booking_step1(request,service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        booking_time =request.POST.get('booking_time')

        if not booking_date or not booking_time:
            messages.error(request, "please select date and time")
            return redirect('booking_step1',service_id)
        
        booking = Booking.objects.create(customer = request.user, service = service, booking_date = booking_date, booking_time = booking_time)

        return redirect('booking_step2', booking.id) 
    
    context={
        'service':service,
        'today':date.today(),
        'tomorrow':date.today()+timedelta(days=1),
        'day_after':date.today()+timedelta(days=2),
    }
    return render(request,'customer/bookings/booking_step1.html',context)



def booking_step2(request,booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    customer_profile = request.user.customerprofile
    addresses = Address.objects.filter(customer = customer_profile) 
    if request.method == "POST":
        address_id = request.POST.get('address')
        if not address_id:
            messages.error(request,"Please select an address")
            return redirect('booking_step2',booking_id)
        
        address = get_object_or_404(Address, id=address_id,customer=customer_profile)
        
        booking.address_line = address.full_address
        booking.city = address.city
        booking.state = address.state
        booking.pincode = address.pincode
        booking.landmark = address.landmark
        booking.save()

        return redirect('booking_step3',booking_id)

    return render(request,'customer/bookings/booking_step2.html',{'booking':booking,'addresses':addresses})



def booking_step3(request):
    if not request.session.get('service_id'):
        return redirect('services')
    return render(request,'customer/bookings/booking_step3.html')


def booking_success(request):
    return render(request,'customer/bookings/booking_success.html')

#-------------------------------------------------------------


def admin_bookings(request):
    return render(request, 'admin/bookings/admin_bookings.html')

def admin_booking_detail(request):
    return render(request, 'admin/bookings/admin_booking_detail.html')
