# bloodbank/urls.py
# from django.urls import path
# from .views import find_blood_bank

# urlpatterns = [
#     path('find/', find_blood_bank, name='find_blood_bank'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('find-blood-bank/', views.find_blood_bank, name='find_blood_bank'),
]

