from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.models import User
from accounts.models import CustomerProfile

# Create your views here.
def admin_customers(request):
    customers = User.objects.filter(is_staff=False, is_superuser=False).annotate(total_bookings = Count("bookings"))

    for user in customers:
        CustomerProfile.objects.get_or_create(user=user, defaults={"full_name":user.get_full_name() or user.username})

    return render(request,'admin/customers_mgnt/admin_customers.html',{'customers':customers})