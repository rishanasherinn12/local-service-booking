from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.customer_login, name = 'customer_login'),
    path('login_admin/', views.login_admin, name = 'login_admin'),
    path('profile/',views.profile, name="profile"),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="customer/acc/password_reset.html",success_url=reverse_lazy('password_reset_done')), name = "password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = "customer/acc/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='customer/acc/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name="password_reset_confirm"),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
            template_name='customer/acc/password_reset_complete.html'),name='password_reset_complete'),


    path('login/', views.google_login_redirect, name='login'),
    path('address/', views.add_address, name = "add_address"),
    path('address/<int:pk>/edit', views.edit_address, name = "edit_address"),
    path('address/<int:pk>/delete', views.delete_address, name = "delete_address"),

#-------------------------------------------------

    path('logout/',views.logout_user,name="logout_user"),
    path('admin_workers/', views.admin_workers, name = "admin_workers"),
    path('admin/add_worker/', views.add_worker, name = "add_worker"),
    path('admin/worker_jobs/', views.worker_jobs, name = "worker_jobs"),
    path('admin/worker_profile/', views.worker_profile, name = "worker_profile"),


]
