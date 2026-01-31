from django.shortcuts import render

# Create your views here.
def admin_customers(request):
    return render(request,'admin/customers_mgnt/admin_customers.html')