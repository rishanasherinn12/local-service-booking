from django.shortcuts import render
from services.models import ServiceCategory, Service, Worker
from bookings.models import Booking, Review
from django.db.models import Count, Avg


# Create your views here.
def home(request):
    categories = ServiceCategory.objects.filter(is_active = True)[:4]
    best_services = Service.objects.filter(is_active=True).annotate(total_bookings=Count("bookings")).order_by("-total_bookings")[:3]
    top_workers = Worker.objects.filter(is_active=True).order_by("-rating")[:4]
    total_customers = Booking.objects.values("customer").distinct().count()
    total_bookings = Booking.objects.count()
    
    context={
        "categories": categories,
        "best_services": best_services,
        "top_workers": top_workers,
        "total_customers": total_customers,
        "total_bookings": total_bookings,
    }
    return render (request,'pages/index.html',context)



def terms(request):
    return render(request,"pages/terms.html")

def privacy(request):
    return render(request,"pages/privacy.html")

def success_stories(request):
    return render(request,"pages/success_stories.html")

def partner_support(request):
    return render(request,"pages/partner_support.html")
