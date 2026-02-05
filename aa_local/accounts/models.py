from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    full_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class Address(models.Model):
    customer =  models.ForeignKey(CustomerProfile, on_delete = models.CASCADE, related_name="address")
    label = models.CharField(max_length=50)
    full_address = models.CharField(max_length=500)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    pincode = models.CharField(max_length = 10)
    landmark = models.CharField(max_length=100, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.label}-{self.city}"