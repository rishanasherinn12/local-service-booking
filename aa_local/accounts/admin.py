from django.contrib import admin
from .models import CustomerProfile,Address

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display=('user','full_name','phone','created_at')


class AddressAdmin(admin.ModelAdmin):
    list_display=('customer','label','full_address','city','state','created_at','pincode','landmark','is_default')

# Register your models here.
admin.site.register(CustomerProfile,CustomerProfileAdmin)
admin.site.register(Address,AddressAdmin)

#class AdressAdmin(admin.ModelAdmin):
