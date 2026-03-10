from django.shortcuts import render
from django.db.models import Sum, Avg
from bookings.models import Booking
from services.models import Worker
from django.utils import timezone
from bookings.models import Booking, Review
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def customer_dashboard(request):
    user = request.user

    
    active_bookings = Booking.objects.filter(
        customer=user,booking_status__in=["PENDING","ASSIGNED","CONFIRMED","IN_PROGRESS"]
    ).count()

    completed_services = Booking.objects.filter(customer=user,booking_status = "COMPLETED").count()
    avg_rating = Review.objects.filter(customer=request.user).aggregate(avg=Avg("rating"))["avg"] or 0
    upcoming_booking = Booking.objects.filter(customer=user,
            booking_date__gte=timezone.now().date(),
            booking_status__in=["ASSIGNED","CONFIRMED","PENDING"]).order_by("booking_date","booking_time").first()
    recent_activity = Booking.objects.filter(customer=user).order_by("-created_at")[:3]
    context = {
        "active_bookings": active_bookings,
        "completed_services": completed_services,
        "avg_rating": round(avg_rating or 0,1),
        "upcoming_booking": upcoming_booking,
        "recent_activity": recent_activity
    }

    return render(request,'customer/dashboard/customer_dashboard.html',context)




@login_required
def admin_dashboard(request):
    total_revenue = Booking.objects.filter(booking_status = "COMPLETED").aggregate(total=Sum("total_price"))["total"] or 0
    total_bookings = Booking.objects.count()
    active_workers = Worker.objects.filter(is_active=True).count()
    pending_requests = Booking.objects.filter(
        booking_status="PENDING").count()
    recent_bookings = Booking.objects.select_related("customer", "service").order_by("-created_at")[:5]
    context ={
        "total_revenue": total_revenue,
        "total_bookings": total_bookings,
        "active_workers": active_workers,
        "pending_requests": pending_requests,
        "recent_bookings": recent_bookings,
    }

    return render(request,'admin/dashboard/admin_dashboard.html',context)