from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, ServiceCategory, Worker
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.views.decorators.cache import never_cache
from .forms import WorkerForm, ServiceForm
from django.db.models import Q


# Create your views here.
@login_required
@never_cache
def services(request):
    category = request.GET.get('category') 
    search = request.GET.get('search','')
    services = Service.objects.select_related('category').all()

    if category and category!= "all":
        services = services.filter(category_id = category)

    if search:
        services = services.filter(Q(title__icontains = search)|Q(description__icontains = search))

    categories = ServiceCategory.objects.filter(is_active = True).distinct()
    
    return render(request,'customer/services/service.html',{'services':services, 'categories': categories, 'selected_category':category, 'search':search})



@login_required
@never_cache
def service_detail(request,id):
    service = Service.objects.get(id=id)
    print(type(service.price))
    tax = service.price * Decimal ("0.18")
    total = service.price + tax
    return render(request,'customer/services/service_detail.html',{'service':service,'tax':tax,'total':total})



#--------------------------------


@login_required
@never_cache
def admin_services(request):
    services = Service.objects.select_related('category').all()
    return render(request,'admin/services/admin_services.html',{'services':services})


@login_required
@never_cache
def add_service(request):
    
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully')
            return redirect('admin_services')
    else:
        form = ServiceForm()
    
    return render(request,'admin/services/add_service.html', {'form':form})


@login_required
def edit_service(request,pk):
    services = get_object_or_404(Service,pk=pk)
    
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance= services)
        if form.is_valid():
            form.save()
            messages.success(request,"Service updated sucessfully!")
            return redirect('admin_services')
    else:
        form = ServiceForm(instance=services)

    return render(request,'admin/services/edit_service.html',{'form':form,"services": services})


def delete_service(request,pk):
    services = get_object_or_404(Service,pk=pk)
    services.delete()
    messages.success(request,"Service deleted successfully!")
    return redirect('admin_services')

@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        icon = request.POST.get("icon")

        ServiceCategory.objects.create(
            name=name,
            icon=icon,
            is_active=True
        )

        messages.success(request, "Category added successfully!")
        return redirect("admin_services")

    return render(request, "admin/services/add_category.html")



def admin_workers(request):
    workers = Worker.objects.all()
    return render(request, 'admin/workers/admin_workers.html',{'workers':workers})  


def add_worker(request):
    if request.method == "POST":
       form = WorkerForm(request.POST, request.FILES)
       if form.is_valid():
           worker = form.save(commit = False) #Don't save yet
           worker.is_active = request.POST.get("is_active") == "true"
           worker.save()
           form.save_m2m()
           
           messages.success(request,"Worker added Successfully")
           return redirect("admin_workers")
    else:
        form = WorkerForm()
    return render(request, 'admin/workers/add_worker.html',{'form':form})  



def worker_jobs(request):
    return render(request, 'admin/workers/worker_jobs.html')  

@login_required
def worker_profile(request,pk):
    worker = get_object_or_404(Worker,pk=pk)

    completed_jobs = worker.bookings.filter(booking_status = "COMPLETED").count()
    total_jobs = worker.bookings.count()
    context = {
        "worker": worker,
        "completed_jobs": completed_jobs,
        "total_jobs": total_jobs,
    }
    return render(request, 'admin/workers/worker_profile.html', context)  
