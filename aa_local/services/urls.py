from django.urls import path
from . import views

urlpatterns=[
    path('',views.services, name='services'),
    path('service_detail/<int:id>',views.service_detail, name='services_detail'),

    path('admin_services/',views.admin_services, name='admin_services'),
    path('add_service/',views.add_service, name='add_service'),
    path('edit_service/<int:pk>/',views.edit_service, name='edit_service'),
    path('delete_service/<int:pk>/',views.delete_service, name='delete_service'),
]