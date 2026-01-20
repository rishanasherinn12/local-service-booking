from django.urls import path
from . import views

urlpatterns=[
    path('',views.booking, name="booking"),
    path('detail/',views.booking_detail, name="booking_detail"),
    
    path('admin/',views.admin_bookings, name="admin_booking"),
    path('admin_detail/',views.admin_booking_detail, name="admin_booking_detail"),
]