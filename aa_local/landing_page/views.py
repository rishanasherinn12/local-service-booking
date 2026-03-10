from django.shortcuts import render
from services.models import ServiceCategory, Service, Worker
from bookings.models import Booking, Review
from django.db.models import Avg


# Create your views here.
def home(request):
    categories = ServiceCategory.objects.filter(is_active = True)[:4]
    best_services = Service.objects.filter(is_active=True,is_best_seller=True)[:6]
    top_workers = Worker.objects.filter(is_active=True).order_by("-rating")[:4]
    total_customers = Booking.objects.values("customer").distinct().count()
    total_bookings = Booking.objects.count()

    best_services = Service.objects.filter(
    is_active=True,
    is_best_seller=True
    ).select_related("category")[:3]
    
    context={
        "categories": categories,
        "best_services": best_services,
        "top_workers": top_workers,
        "total_customers": total_customers,
        "total_bookings": total_bookings,
        "best_services": best_services,
    }
    return render (request,'pages/index.html',context)