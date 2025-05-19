# admins/urls.py
from django.urls import path
from admins.views import dashboard
from .views import admin_login
from . import views


urlpatterns = [
    path('admin_login/', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('manage-drives/', views.manage_donation_drives, name='manage_donation_drives'),
    path('approve-drive/<int:drive_id>/', views.approve_drive, name='approve_drive'),
    path('reject-drive/<int:drive_id>/', views.reject_drive, name='reject_drive'),
]
