from django.shortcuts import render, redirect, get_object_or_404
from services.models import Service 
from accounts.models import Address
from .models import Booking, Payment, Review
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

from django.contrib.admin.views.decorators import staff_member_required
from .forms import BookingAssignForm

from django.db.models import Case, When, Value, IntegerField, Avg


# Create your views here.
@login_required
def booking(request):
    tab = request.GET.get("tab","upcoming") #default upcoming
    bookings=Booking.objects.select_related('service','worker','payment').filter(customer=request.user).order_by('-created_at')
    upcoming = bookings.filter(booking_status__in=["PENDING", "ASSIGNED", "CONFIRMED", "IN_PROGRESS"]).annotate(
        priority=Case(
        When(booking_status="IN_PROGRESS", then=Value(1)),
        When(booking_status="ASSIGNED", then=Value(2)),
        When(booking_status="CONFIRMED", then=Value(3)),
        When(booking_status="PENDING", then=Value(4)),
        output_field=IntegerField()
    )
    ).order_by("priority","booking_date","booking_time")

    history = bookings.filter(booking_status__in=["COMPLETED", "CANCELLED"]).order_by("-updated_at")   
    banner = None
    
    if tab == "upcoming":
        if upcoming.filter(booking_status="ASSIGNED").exists():
            banner = "ASSIGNED"
        elif upcoming.filter(booking_status="PENDING").exists():
            banner = "PENDING"

    context={"banner":banner,"upcoming":upcoming,"history":history,"active_tab":tab}

    return render(request,'customer/bookings/my_bookings.html', context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.booking_status in ["PENDING","ASSIGNED"]:
        booking.booking_status = "CANCELLED"
        booking.save()
        messages.success(request,"Booking cancelled successfully.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
    return redirect("booking")




def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer = request.user)
    return render(request,'customer/bookings/booking_detail.html',{'booking':booking})


@login_required
def booking_step1(request,service_id):
    
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        booking_time =request.POST.get('booking_time')

        if not booking_date or not booking_time:
            messages.error(request, "please select date and time")
            return redirect('booking_step1',service_id)
        
        service_price = service.price
        tax = service_price * Decimal("0.18")
        total_amount = service_price + tax

        existing_booking = Booking.objects.filter(customer = request.user, service = service, booking_status = "PENDING").first()
        if existing_booking:
            existing_booking.booking_date = booking_date
            existing_booking.booking_time = booking_time
            existing_booking.total_price = total_amount
            existing_booking.booking_status = "PENDING"
            existing_booking.created_at = timezone.now() #moves reused booking to top
            existing_booking.save()
            return redirect("booking_step2",existing_booking.id)
                    
        booking = Booking.objects.create(customer = request.user, service = service, booking_date = booking_date, booking_time = booking_time, total_price=total_amount,booking_status="PENDING")

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
        messages.info(request,"Your booking request has been submitted. Payment will be enabled after a professional is assigned.")
        #-------------------------
        flow = request.GET.get("flow")
        if flow == "payment":
            return redirect(f'/booking/booking_step3/{booking.id}?flow=payment')
        # #---------------------------------
        return redirect('booking')

    return render(request,'customer/bookings/booking_step2.html',{'booking':booking,'addresses':addresses})



def booking_step3(request,booking_id):
    booking= get_object_or_404(Booking, id=booking_id, customer=request.user)

    # Only allow payment after admin assigns worker
    if booking.booking_status != "ASSIGNED":
        messages.error(request, "Waiting for admin approval before payment.")
        return redirect("booking")

    service_price = booking.service.price
    tax = service_price * Decimal("0.18")
    total_amount = service_price + tax
    came_from_payment = request.GET.get("flow") == "payment"
    context={"booking":booking,"service_price":service_price,"tax":tax,"total_amount":total_amount,"came_from_payment":came_from_payment}
   
    return render(request,'customer/bookings/booking_step3.html',context)


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id,customer=request.user)
    payment = booking.payment
    payment.status = 'SUCCESS'
    payment.paid_at = timezone.now()
    payment.save()

    booking.booking_status = 'CONFIRMED'
    booking.save()
    return render(request,'customer/bookings/booking_success.html', {'booking':booking})



def stripe_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.booking_status != "ASSIGNED":
        messages.error(request, "Booking not approved yet.")
        return redirect("booking")
    
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
            if payment.status != "SUCCESS":
                with transaction.atomic():
                    payment.status = "SUCCESS"
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


@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking,id=booking_id, customer=request.user)
    if request.method == "POST":
        rating=request.POST.get("rating")
        comment=request.POST.get("comment")

        Review.objects.create(booking=booking,customer=request.user,worker=booking.worker, rating=rating,comment=comment)
        avg = Review.objects.filter(worker=booking.worker).aggregate(avg=Avg("rating"))["avg"]
        booking.worker.rating=round(avg, 2)
        booking.worker.save()
    return redirect("booking")
    

#-------------------------------------------------------------



@staff_member_required
def admin_bookings(request):
    from django.db.models import Case, When, Value, IntegerField
    # expiry_time = timezone.now() - timedelta(minutes=30)
    # # Mark old REQUESTED bookings as CANCELLED
    # Booking.objects.filter(booking_status="REQUESTED",created_at__lt=expiry_time).update(booking_status="CANCELLED")

    bookings = Booking.objects.filter(booking_status__in = ["PENDING","ASSIGNED", "CONFIRMED"]).select_related(
        "customer","service","worker").annotate(
            priority=Case(
                When(booking_status="PENDING", then=Value(1)),
                When(booking_status="ASSIGNED", then=Value(2)),
                When(booking_status="CONFIRMED", then=Value(3)),
                output_field=IntegerField()
            )
        ).order_by("priority","-created_at") #pending first

    context = {"bookings":bookings}
    return render(request, 'admin/bookings/admin_bookings.html',context)


@staff_member_required
def admin_booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    from_page = request.GET.get("from")

    if request.method == "POST":
        form = BookingAssignForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            if booking.worker: #worker stored in booking
                booking.booking_status = "ASSIGNED"
            booking.save()  #worker is saved
            return redirect('admin_booking_detail', booking_id = booking.id)
    else:
        form = BookingAssignForm(instance = booking)

    return render(request, 'admin/bookings/admin_booking_detail.html',{'booking':booking,'form':form,"from_page": from_page})








