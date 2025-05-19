# raktkan/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from donors.models import Donor
from recipients.models import Recipient
from bloodbanks.models import BloodBank
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count

def register_choice(request):
    # A simple page that gives a choice to register as a donor or recipient
    return render(request, "register.html")

def home_view(request):
    # Get total counts for stats (e.g., total users, donors, recipients, blood banks)
    total_users = Donor.objects.count() + Recipient.objects.count()
    total_donors = Donor.objects.count()
    total_recipients = Recipient.objects.count()
    total_blood_banks = BloodBank.objects.count()

        # Get the top donors by donation count
    top_donors = Donor.objects.order_by('-donation_count')[:5]

    return render(request, 'home.html', {
        'total_users': total_users,
        'total_donors': total_donors,
        'total_recipients': total_recipients,
        'total_blood_banks': total_blood_banks,
        'top_donors': top_donors
    })

def register(request):
    # Render a registration choice page (Donor or Recipient)
    return render(request, 'register.html')