from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_customers, name = 'admin_customers'),
    
]