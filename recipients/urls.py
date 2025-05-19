# # recipient/urls.py
# from django.urls import path
# from .views import recipient_register, recipient_dashboard
# from .views import recipient_login,logout_view,find_donors,your_request


# urlpatterns = [
#     path('register/', recipient_register, name='recipient_register'),
#     path('dashboard/', recipient_dashboard, name='recipient_dashboard'),
#     path("login/", recipient_login, name="recipient_login"),
#     path('logout/', logout_view, name='logout'),
#     path('find-donors/',find_donors, name='find_donors'),
#     path('your-request/', your_request, name='your_request'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.recipient_register, name="recipient_register"),
    path("login/", views.recipient_login, name="recipient_login"),
    path("logout/", views.logout_view, name="recipient_logout"),
    path("dashboard/", views.recipient_dashboard, name="recipient_dashboard"),
    path("profile/", views.recipient_profile, name="recipient_profile"),
    path("find-blood-banks/", views.find_blood_banks, name="find_blood_banks"),
    path('find_donors/', views.find_donors, name='find_donors'),
    path('your-requests/', views.your_request, name='your_request'),
    path('create-request/', views.create_blood_request, name='create_blood_request'),
    path("cancel-request/", views.cancel_blood_request, name="cancel_blood_request"),
     path('profile/', views.recipient_profile, name='recipient_profile'),
    path('edit-profile/', views.edit_recipient_profile, name='edit_recipient_profile'),
    path('change-password/', views.change_recipient_password, name='change_recipient_password'),

]

