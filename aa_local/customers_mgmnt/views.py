from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from accounts.models import CustomerProfile
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

# Create your views here.
@staff_member_required
@never_cache
def admin_customers(request):
    customers = User.objects.filter(is_staff=False, is_superuser=False).annotate(total_bookings = Count("bookings"))

    for user in customers:
        CustomerProfile.objects.get_or_create(user=user, defaults={"full_name":user.get_full_name() or user.username})

    return render(request,'admin/customers_mgnt/admin_customers.html',{'customers':customers})


@staff_member_required
@never_cache
def block_customer(request,user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_satff:
        messages.error(request,"Admin accounts cannot be blocked")
        return redirect("admin_customers")
    
    if user == request.user:
        messages.error(request,"You cannot block yourself.")
        return redirect("admin_customers")
    
    user.is_active = False
    user.save()
    messages.success(request,'Customer blocked successfully')
    return redirect('admin_customers')


@staff_member_required
@never_cache
def unblock_customer(request,user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "Customer unblocked successfully")
    return redirect('admin_customers')