from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from donationdrive.models import DonationDrive



def manage_donation_drives(request):
    pending_drives = DonationDrive.objects.filter(approved=False)
    return render(request, 'admins/manage_drives.html', {'pending_drives': pending_drives})

def approve_drive(request, drive_id):
    drive = get_object_or_404(DonationDrive, id=drive_id)
    drive.approved = True
    drive.save()
    return redirect('manage_donation_drives')

def reject_drive(request, drive_id):
    drive = get_object_or_404(DonationDrive, id=drive_id)
    drive.delete()
    return redirect('manage_donation_drives')

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate Admin (checks username & password)
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Only allow admin users
            login(request, user)
            return redirect("dashboard")  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid Credentials or Not an Admin")
    
    return render(request, 'admins/admin_login.html')

def dashboard(request):
    return render(request, 'admins/dashboard.html')
