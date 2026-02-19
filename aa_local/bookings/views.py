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

stripe.api_key = settings.STRIPE_SECRET_KEY

#stripe webhook
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone


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
        
        booking.label = address.label
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


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request,'customer/bookings/booking_success.html', {'booking':booking})



def stripe_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.service.price < 50:
        messages.error(request,"Online payment requires minimum ₹50.")
        return redirect("booking_step3", booking.id)
     # Amount must be in paisa (INR) => multiply by 100
    amount = int(booking.service.price * 100) 

    success_url = request.build_absolute_uri(reverse('booking_success', args=[booking.id]))+"?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(reverse('booking_step3', args=[booking.id]))

    #Create stripe session
    session = stripe.checkout.Session.create(payment_method_types=['card'],mode='payment',line_items=[{
        'price_data':{'currency':'inr','product_data':{'name':booking.service.title,},'unit_amount':amount,},
        'quantity':1,
    }],
    success_url=success_url,
    cancel_url=cancel_url,
    )
    
    # Create or update Payment record
    payment,created = Payment.objects.get_or_create(booking=booking, defaults={
        "amount":booking.service.price,
        "status":"PENDING"
    })
    payment.stripe_session_id = session.id
    payment.save()
    return redirect(session.url)




@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return HttpResponse(status=400)
    
    #payment successfull
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id")
        payment_intent = session.get("payment_intent")
        try:
            payment = Payment.objects.get(stripe_session_id = session_id)
            with transaction.atomic():
                payment.payment_status = "SUCCESS"
                payment.stripe_payment_intent = payment_intent
                payment.paid_at = timezone.now()
                payment.save()

            # Optional: Update booking status
            booking = payment.booking
            booking.booking_status = "CONFIRMED"
            booking.save()

        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)


#-------------------------------------------------------------




def admin_bookings(request):
    return render(request, 'admin/bookings/admin_bookings.html')

def admin_booking_detail(request):
    return render(request, 'admin/bookings/admin_booking_detail.html')




