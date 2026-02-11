from django.contrib import admin

from .models import Booking,Payment

class BookingAdmin(admin.ModelAdmin):
    list_display=('customer','service','worker','booking_date','booking_time','booking_status','created_at','updated_at')

class PaymentAdmin(admin.ModelAdmin):
    list_display=('booking','amount','status','created_at','stripe_payment_intent')


# Register your models here.
admin.site.register(Booking,BookingAdmin)
admin.site.register(Payment,PaymentAdmin)