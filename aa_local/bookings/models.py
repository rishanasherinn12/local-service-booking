from django.db import models
from django.contrib.auth.models import User
from services.models import Service,Worker


# Create your models here.
class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('ASSIGNED', 'Assigned'),
        ('CONFIRMED','Confirmed'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete = models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete = models.CASCADE, related_name='bookings')
    worker = models.ForeignKey(Worker, on_delete = models.SET_NULL, null=True, blank=True, related_name='bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()

    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    label = models.CharField(max_length=50, blank=True, null=True)
    address_line = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=100, blank=True)

    booking_status = models.CharField(max_length=20, choices = BOOKING_STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Booking #{self.id} - {self.service.title}"
    

class Payment(models.Model):
    PAYMENT_STATUS =[
        ('PENDING','Pending'),
        ('SUCCESS','Success'),
        ('FAILED','Failed'),
    ]

    PAYMENT_METHOD = [
        ('COD','Cash on Delivery'),
        ('ONLINE','Online Payment'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default="ONLINE")
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True,null=True)
    
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"
