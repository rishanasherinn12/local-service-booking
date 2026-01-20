from django.shortcuts import render

# Create your views here.
def booking(request):
    return render(request,'customer/bookings/my_bookings.html')

def booking_detail(request):
    return render(request,'customer/bookings/booking_detail.html')






def admin_bookings(request):
    return render(request, 'admin/bookings/admin_bookings.html')

def admin_booking_detail(request):
    return render(request, 'admin/bookings/admin_booking_detail.html')
