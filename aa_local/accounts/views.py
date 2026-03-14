from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import CustomerProfile, Address
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import RegisterForm,CustomerProfileForm, AddressForm



# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():

            #  Check duplicate phone
            if CustomerProfile.objects.filter(phone=form.cleaned_data['phone']).exists():
                messages.error(request, "Phone number already registered")
                return redirect('register')

            user = form.save(commit = False)
            user.email = form.cleaned_data['email']
            user.save()
            CustomerProfile.objects.create(user = user, phone = form.cleaned_data['phone'])
            messages.success(request,'Account created successfully')
            return redirect('customer_login')
        else:
            # Push form errors into messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('register')   
    form = RegisterForm()
    return render(request, 'customer/acc/register_customer.html', {'form': form})



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




# @login_required
# @never_cache
# def profile(request):
#     profile = request.user.customer_profile
#     address = profile.address.all()

#     if request.method == "POST":
#         full_name = request.POST.get('full_name','').strip()
#         phone = request.POST.get('phone','').strip()
#         if full_name:
#             profile.full_name = full_name
#         if phone:
#             profile.phone = phone
#         profile.save()
#         messages.success(request,'profile updated successfully')
#         return redirect('profile')
    
#     return render(request,'customer/acc/profile.html',{'profile':profile, 'address':address,})

@login_required
@never_cache
def profile(request):
    profile,created = CustomerProfile.objects.get_or_create(user = request.user, defaults ={
        "full_name":request.user.get_full_name() or request.user.username
    })
    address = profile.address.all()

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance = profile)
        if form.is_valid():
            form.save()

            messages.success(request,'profile updated successfully')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request,error)
            return redirect('profile')
    form = CustomerProfileForm(instance=profile)
    
    return render(request,'customer/acc/profile.html',{'profile':profile, 'address':address,'form':form})



@login_required(login_url='customer_login')
def add_address(request):
    customer = CustomerProfile.objects.get(user = request.user)
    next_url = request.GET.get('next')  # ✅ capture redirect url
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit = False)
            # address.customer = request.user.customer_profile
            address.customer = customer
            # convert checkbox value properly
            address.is_default = request.POST.get("is_default") == "on"

            # ensure only one default address
            if address.is_default:
                Address.objects.filter(customer=customer).update(is_default=False)

            if not Address.objects.filter(customer=customer, is_default=True).exists():
                address.is_default = True

            address.save()
        
            messages.success(request, "Address added successfully")

            # ✅ redirect back to booking step2 if next exists
            if next_url:
                return redirect(next_url)
            
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('add_address')
    form = AddressForm()
    
    return render(request, 'customer/acc/add_address.html',{'form':form,'next_url': next_url})




@login_required
def edit_address(request, pk):
    profile = request.user.customer_profile
    address = get_object_or_404(Address, pk=pk, customer=profile)
    if request.method == "POST":
        form = AddressForm(request.POST, instance = address)
        if form.is_valid():
            address = form.save(commit=False)
            address.is_default = request.POST.get("is_default") == "on"
            # ensure only one default address
            if address.is_default:
                Address.objects.filter(customer=profile).exclude(pk=address.pk).update(is_default=False)

            address.save()
            messages.success(request,'Address Updated Successfully')
            return redirect('profile')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request,error)
            return redirect('edit_address',pk)
        
    form = AddressForm(instance = address)
    return render(request,'customer/acc/edit_address.html',{'form':form,'address':address})
    


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


