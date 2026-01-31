from django.shortcuts import render, redirect

# Create your views here.
def booking(request):
    return render(request,'customer/bookings/my_bookings.html')

def booking_detail(request):
    return render(request,'customer/bookings/booking_detail.html')


def booking_step1(request,service_id):
    request.session['service_id'] = service_id   #save srvc_id in session
    return render(request,'customer/bookings/booking_step1.html',{'service_id': service_id})



def booking_step2(request):
    service_id = request.session.get('service_id')  #read srvc_id from session
    if not service_id:
        return redirect('services')
    return render(request,'customer/bookings/booking_step2.html',{'service_id':service_id})



def booking_step3(request):
    if not request.session.get('service_id'):
        return redirect('services')
    return render(request,'customer/bookings/booking_step3.html')


def booking_success(request):
    return render(request,'customer/bookings/booking_success.html')

#-------------------------------------------------------------


def admin_bookings(request):
    return render(request, 'admin/bookings/admin_bookings.html')

def admin_booking_detail(request):
    return render(request, 'admin/bookings/admin_booking_detail.html')
