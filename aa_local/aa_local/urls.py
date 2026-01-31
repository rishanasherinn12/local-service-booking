from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing_page.urls')),
    path('acc/', include('accounts.urls')),
    path('booking/', include('bookings.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('services/', include('services.urls')),
    path('customers/', include('customers_mgmnt.urls')),

    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)