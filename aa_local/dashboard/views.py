from django.shortcuts import render

# Create your views here.
def customer_dashboard(request):
    return render(request,'customer/dashboard/customer_dashboard.html')

def admin_dashboard(request):
    return render(request,'admin/dashboard/admin_dashboard.html')