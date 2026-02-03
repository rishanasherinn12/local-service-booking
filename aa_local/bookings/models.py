from django.db import models
from django.contrib.auth.models import User
from .models import Service, Worker


# Create your models here.
class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('REQUESTED','Requested'),
        ('CONFIRMED','Confirmed'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    ]
    customer = models.ForeignKey(User, on_delete = models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete = models.CASCADE, related_name='bookings')
    worker = models.ForeignKey(Worker, on_delete = models.SET_NULL, null=True, blank=True, related_name='bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()

    address_line = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=100, blank=True)

    booking_status = models.CharField(max_length=20, choices = BOOKING_STATUS_CHOICES, default='REQUESTED')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Booking #{self.id}"