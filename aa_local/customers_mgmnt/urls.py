from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_customers, name = 'admin_customers'),
    path('block/<int:user_id>/', views.block_customer, name = 'block_customer'),
    path('uunblock/<int:user_id>/', views.unblock_customer, name = 'unblock_customer'),
    
]