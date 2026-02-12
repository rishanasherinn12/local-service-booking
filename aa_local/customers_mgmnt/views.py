from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from accounts.models import CustomerProfile
from django.contrib import messages

# Create your views here.
def admin_customers(request):
    customers = User.objects.filter(is_staff=False, is_superuser=False).annotate(total_bookings = Count("bookings"))

    for user in customers:
        CustomerProfile.objects.get_or_create(user=user, defaults={"full_name":user.get_full_name() or user.username})

    return render(request,'admin/customers_mgnt/admin_customers.html',{'customers':customers})


def block_customer(request,user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request,'Customer blocked successfully')
    return redirect('admin_customers')

def unblock_customer(request,user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "Customer unblocked successfully")
    return redirect('admin_customers')