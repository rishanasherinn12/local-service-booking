from django.shortcuts import render, redirect, get_object_or_404
from services.models import Service 
from accounts.models import Address
from .models import Booking, Payment
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.contrib import messages
from decimal import Decimal

import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEYS


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
    customer_profile = request.user.customer_profile
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



def booking_step3(request,booking_id):
    booking= get_object_or_404(Booking, id=booking_id, customer=request.user)
    service_price = booking.service.price
    tax = service_price * Decimal("0.18")
    total_amount = service_price + tax

    context={"booking":booking,"service_price":service_price,"tax":tax,"total_amount":total_amount}
   
    return render(request,'customer/bookings/booking_step3.html',context)


def booking_success(request):
    return render(request,'customer/bookings/booking_success.html')



def stripe_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
     # Amount must be in paisa (INR) => multiply by 100
    amount = int(booking.service.price * 100) 

    #Create stripe session
    session = stripe.checkout.Session.create(payment_method_types=['card'],mode='payment',line_items=[{
        'price_data':{'currency':'inr','product_data':{'name':booking.service.title,},'unit_amount':amount,},
        'quantity':1,
    }])

    success_url = request.build_absolute_uri(reverse('stripe_success'))+"?session_id={CHECKOUT_SESSION_ID}",
    cancel_url = request.build_absolute_uri(reverse('stripe_cancel')),

    # Create or update Payment record
    payment,created = Payment.objects.get_or_create(booking=booking, defaults={
        "amount":booking.service.price,
        "payment_status":"PENDING"
    })
    payment.stripe_session_id = session.id
    payment.save()
    return redirect(session.url)



def stripe_success(request):
    return render(request,"customer/stripe_success.html")

def stripe_cancel(request):
    return render(request, "customer/stripe_cancel.html")

#-------------------------------------------------------------




def admin_bookings(request):
    return render(request, 'admin/bookings/admin_bookings.html')

def admin_booking_detail(request):
    return render(request, 'admin/bookings/admin_booking_detail.html')
