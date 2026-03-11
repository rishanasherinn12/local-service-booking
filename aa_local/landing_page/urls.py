from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("success-stories/", views.success_stories, name="success_stories"),
    path("partner-support/", views.partner_support, name="partner_support"),

    
]
