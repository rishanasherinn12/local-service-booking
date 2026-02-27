from django.contrib import admin
from .models import ServiceCategory, Service, Worker
from django.utils.html import format_html

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display=('name','icon','is_active')

class ServiceAdmin(admin.ModelAdmin):
    list_display=('title','category','price', 'image_preview','includes','is_active')

    def image_preview(self,obj):
        if obj.image:
            return format_html('<img src="{}" width="60" style="object-fit:cover;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"

class WorkerAdmin(admin.ModelAdmin):
    list_display=('full_name','display_services','photo','rating','is_active','email','location',)
    def display_services(self, obj):
        return ", ".join(service.title for service in obj.services.all())

    display_services.short_description = "Services"
    

# Register your models here.
admin.site.register(ServiceCategory,ServiceCategoryAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Worker,WorkerAdmin)



