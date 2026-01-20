from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import CustomerProfile, Address
from django.contrib.auth.decorators import login_required



# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request,'username already taken')
            return redirect('register')
        
        if User.objects.filter(email = email).exists():
            messages.error(request,'email already taken')
            return redirect('register')
        
        if CustomerProfile.objects.filter(phone = phone).exists():
            messages.error(request,'phone no already taken')
            return redirect('register')
        
        user = User.objects.create_user(username = username, email = email, password = password)
        user.save()
        CustomerProfile.objects.create(user = user, phone = phone)
        messages.success(request,'Account created successfully')
        return redirect('customer_login')
        

    return render(request, 'customer/acc/register_customer.html')




def customer_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username , password =password)     

        if user is not None:
            login(request, user) #create session
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('customer_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('customer_login')
            
    return render(request, 'customer/acc/login_customer.html')



def google_login_redirect(request):
    return redirect('/accounts/google/login/')




@login_required
def profile(request):
    profile = request.user.customer_profile
    address = profile.address.all()

    if request.method == "POST":
        full_name = request.POST.get('full_name','').strip()
        phone = request.POST.get('phone','').strip()
        if full_name:
            profile.full_name = full_name
        if phone:
            profile.phone = phone
        profile.save()
        messages.success(request,'profile updated successfully')
        return redirect('profile')
    
    return render(request,'customer/acc/profile.html',{'profile':profile, 'address':address,})



@login_required(login_url='customer_login')
def add_address(request):
    customer = CustomerProfile.objects.get(user = request.user)
    if request.method == "POST":
        label = request.POST.get('label')
        full_address = request.POST.get('full_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark')
        Address.objects.create(customer = customer, label = label, full_address = full_address, city = city, state = state, pincode = pincode, landmark = landmark)
        messages.success(request, "Adress added successfully")
        return redirect('profile')
    
    return render(request, 'customer/acc/add_address.html')


@login_required
def edit_address(request, pk):
    profile = request.user.customer_profile
    address = get_object_or_404(Address, pk=pk, customer=profile)
    if request.method == "POST":
        address.label = request.POST.get('label')
        address.full_address = request.POST.get('full_address')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.pincode = request.POST.get('pincode')
        address.landmark = request.POST.get('landmark')
        address.is_default = bool(request.POST.get('is_default'))
        address.save()

        messages.success(request,'Address Updated Successfully')
        return redirect('profile')
    
    return render(request, 'customer/acc/edit_address.html',{'address':address})


@login_required
def delete_address(request,pk):
    profile = request.user.customer_profile
    address = get_object_or_404(Address, pk=pk, customer=profile)

    address.delete()
    messages.success(request,"Address deleted")
    return redirect('profile')

#-------------------------------------------------------------------

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


def login_admin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:

            if user.is_staff:
                login(request,user)
                return redirect('admin_dashboard')
            else:
                messages.error(request,'you are not authorized as admin')
                return redirect('login_admin')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login_admin')

    return render(request,'admin/acc/login_admin.html')



def admin_workers(request):
    return render(request, 'admin/workers/admin_workers.html')  

def add_worker(request):
    return render(request, 'admin/workers/add_worker.html')  

def worker_jobs(request):
    return render(request, 'admin/workers/worker_jobs.html')  

def worker_profile(request):
    return render(request, 'admin/workers/worker_profile.html')  
