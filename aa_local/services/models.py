from django.db import models

# Create your models here.
class ServiceCategory(models.Model):
    name = models.CharField(max_length = 100)
    icon = models.CharField(max_length = 100,blank=True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name = "services")
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    duration_minutes = models.IntegerField()
    image = models.ImageField(upload_to="services/",blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title