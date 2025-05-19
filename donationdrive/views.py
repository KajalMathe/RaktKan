from django.shortcuts import render, redirect
from .models import DonationDrive
from .forms import DonationDriveForm
from django.utils import timezone

def donation_drive_list(request):
    drives = DonationDrive.objects.filter(
    approved=True,
    end_date__gte=timezone.now().date()  # show only ongoing/upcoming
).order_by('start_date') 
    return render(request, 'donation_drive/donationdrive.html', {'drives': drives})

def donation_drive_thankyou(request):
    return render(request, 'donation_drive/thankyou.html')

from .forms import DonationDriveForm

def drive_register(request):
    if request.method == 'POST':
        form = DonationDriveForm(request.POST, request.FILES)
        if form.is_valid():
            drive = form.save(commit=False)
            drive.approved = False  # Require admin approval
            drive.save()
            return redirect('donation_drive_thankyou')
    else:
        form = DonationDriveForm()

    return render(request, 'donation_drive/drive_register.html', {'form': form})

