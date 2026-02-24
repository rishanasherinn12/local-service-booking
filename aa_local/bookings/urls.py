from django.urls import path
from . import views

urlpatterns=[
    path('',views.booking, name="booking"),
    path('detail/<int:booking_id>/',views.booking_detail, name="booking_detail"),
    path('booking_step1/<int:service_id>/',views.booking_step1, name="booking_step1"),
    path('booking_step2/<int:booking_id>',views.booking_step2, name="booking_step2"),
    path('booking_step3/<int:booking_id>',views.booking_step3, name="booking_step3"),
    path('booking_success/<int:booking_id>',views.booking_success, name="booking_success"),
    
    path("stripe/checkout/<int:booking_id>/", views.stripe_checkout, name="stripe_checkout"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
    
    path('admin/',views.admin_bookings, name="admin_booking"),
    path('admin_detail/<int:booking_id>/',views.admin_booking_detail, name="admin_booking_detail"),
]