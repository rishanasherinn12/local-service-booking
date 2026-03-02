from django.urls import path
from . import views

urlpatterns=[
    path('',views.services, name='services'),
    path('service_detail/<int:id>',views.service_detail, name='services_detail'),

    path('admin_services/',views.admin_services, name='admin_services'),
    path('add_service/',views.add_service, name='add_service'),
    path('edit_service/<int:pk>/',views.edit_service, name='edit_service'),
    path('delete_service/<int:pk>/',views.delete_service, name='delete_service'),
    path('add_category/',views.add_category, name='add_category'),

    path('admin_workers/', views.admin_workers, name = "admin_workers"),
    path('admin/add_worker/', views.add_worker, name = "add_worker"),
    path('admin/edit_worker/<int:pk>', views.edit_worker, name = "edit_worker"),
    path('admin/worker_jobs/<int:pk>/', views.worker_jobs, name = "worker_jobs"),
    path('admin/worker_profile/<int:pk>/', views.worker_profile, name = "worker_profile"),

]