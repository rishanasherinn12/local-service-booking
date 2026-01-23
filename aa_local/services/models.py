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
    is_best_seller = models.BooleanField(default=False)
    includes = models.TextField(blank=True,default="",
        help_text="Enter one item per line (e.g. Deep dusting, Floor cleaning, etc.)"
    )

    def __str__(self):
        return self.title
    

class Worker(models.Model):
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20,unique=True)
    photo = models.ImageField(upload_to="workers/",blank=True,null=True)
    rating = models.DecimalField(max_digits=3,decimal_places=2,default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name