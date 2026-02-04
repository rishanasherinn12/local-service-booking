from django.contrib import admin

from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display=('customer','service','worker','booking_date','booking_time','booking_status','created_at','updated_at')

# Register your models here.
admin.site.register(Booking,BookingAdmin)