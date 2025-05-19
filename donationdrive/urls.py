from django.urls import path
from . import views

urlpatterns = [
    path('donation_drive/', views.donation_drive_list, name='donation_drive'),
    path('drive_register/', views.drive_register, name='register_drive'),
    path('thankyou/', views.donation_drive_thankyou, name='donation_drive_thankyou'),
]
