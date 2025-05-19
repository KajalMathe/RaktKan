# # donor/urls.py
# from django.urls import path
# from donors import views
# from .views import donor_register, donor_dashboard, leaderboard,donor_login

# urlpatterns = [
#     path('register/', donor_register, name='donor_register'),
#     path('dashboard/', donor_dashboard, name='donor_dashboard'),
#     path('leaderboard/', leaderboard, name='leaderboard'),
#     path("login/", donor_login, name="donor_login"),
#     path('profile/', views.donor_profile, name='donor_profile'),
#     path('schedule/', views.schedule_donation, name='schedule_donation'),
#     path('impact/', views.my_impact, name='my_impact'),
#     path('resources/', views.resources, name='resources'),
#     path('community/', views.community, name='community'),
#     path('faq/', views.faq, name='faq'),
#     path('logout/', views.logout_view, name='logout'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.donor_register, name="donor_register"),
    path("login/", views.donor_login, name="donor_login"),
    path("logout/", views.logout_view, name="donor_logout"),
    path("dashboard/", views.donor_dashboard, name="donor_dashboard"),
    path("profile/", views.donor_profile, name="donor_profile"),
    path("impact/", views.my_impact, name="my_impact"),
    path("schedule/", views.schedule_donation, name="schedule_donation"),
    path("resources/", views.resources, name="resources"),
    path("community/", views.community, name="community"),
    path("faq/", views.faq, name="faq"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('change-password/', views.change_donor_password, name='change_donor_password'),
    path("forgot-password/", views.forgot_password_page, name="donor_forgot_password"),
    path("reset-password/", views.reset_donor_password, name="donor_reset_password"),
    
]
