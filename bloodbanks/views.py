# bloodbank/views.py
from django.shortcuts import render
from .models import BloodBank

def find_blood_bank(request):
    # Check based on session
    if request.session.get('recipient_id'):
        base_template = 'recipients/base1.html'
    else:
        base_template = 'base.html'

    bloodbanks = BloodBank.objects.all()

    context = {
        'base_template': base_template,
        'bloodbanks': bloodbanks,
    }
    return render(request, 'bloodbanks/find_blood_bank.html', context)


    

