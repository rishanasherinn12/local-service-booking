from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, ServiceCategory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.views.decorators.cache import never_cache


# Create your views here.
@login_required
@never_cache
def services(request):
    services = Service.objects.select_related('category').all()
    return render(request,'customer/services/service.html',{'services':services})

@login_required
@never_cache
def service_detail(request,id):
    service = Service.objects.get(id=id)
    print(type(service.price))
    tax = service.price * Decimal (0.18)
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
    categories = ServiceCategory.objects.filter(is_active = True)
    if request.method == "POST":
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration_minutes = request.POST.get('duration_minutes')
        image = request.FILES.get('image')
        status = request.POST.get('status')
        includes = request.POST.get('includes')

        category = get_object_or_404(ServiceCategory, id=category_id)

        Service.objects.create(title = title, category=category, description=description,includes=includes, 
                               price=price, duration_minutes=duration_minutes, image=image, is_active=True if status == "active" else False)
        messages.success(request, 'Service added successfully')
        return redirect('admin_services')

    return render(request,'admin/services/add_service.html', {'categories':categories})

@login_required
def edit_service(request,pk):
    services = get_object_or_404(Service,pk=pk)
    categories = ServiceCategory.objects.filter(is_active=True)
    if request.method == "POST":
        services.title = request.POST.get('title')

        services.category = get_object_or_404(ServiceCategory,id=request.POST.get('category'))
        services.description = request.POST.get('description')
        services.includes = request.POST.get('includes')
        services.price = request.POST.get('price')
        services.duration_minutes = request.POST.get('duration_minutes')
        services.is_active = True if request.POST.get('status') == "active" else False

        if 'image' in request.FILES:
            services.image = request.FILES['image']

        services.save()
        messages.success(request,"Service updated sucessfully!")
        return redirect('admin_services')

    return render(request,'admin/services/edit_service.html',{'services':services,'categories':categories})

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
