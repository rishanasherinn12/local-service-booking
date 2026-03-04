from django.shortcuts import render
from django.db.models import Sum
from bookings.models import Booking
from services.models import Worker


# Create your views here.
def customer_dashboard(request):
    return render(request,'customer/dashboard/customer_dashboard.html')

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