# # donor/views.py
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# # from .models import DonorProfile
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from .forms import DonorRegistrationForm
# from .models import Donor
# from django.contrib import messages
# from django.contrib.auth import logout
# from django.shortcuts import render, redirect
# from django.utils.timezone import now
# import logging

# # Set up logging for debugging
# logger = logging.getLogger(__name__)

# def donor_register(request):
#     if request.method == "POST":
#         form = DonorRegistrationForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             try:
#                 donor = form.save(commit=False)

#                 # ✅ Explicitly set required fields if not present
#                 if not donor.date_joined:
#                     donor.date_joined = now()

#                 if donor.donation_count is None:
#                     donor.donation_count = 0  # Default to 0

#                 donor.save()

#                 login(request, donor)
#                 messages.success(request, "Registration successful! Welcome to RaktKan.")
#                 return redirect("donor_dashboard")

#             except Exception as e:
#                 logger.error(f"Error during donor registration: {e}")
#                 messages.error(request, "An error occurred during registration. Please try again.")

#         else:
#             logger.warning(f"Form validation errors: {form.errors}")  # ✅ Log errors
#             messages.error(request, "Please correct the errors below.")

#     else:
#         form = DonorRegistrationForm()

#     return render(request, "donors/donor_register.html", {"form": form})





# def donor_login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")  # Use "username" instead of "email"
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("donor_dashboard")  # Redirect to donor dashboard after login
#         else:
#             messages.error(request, "Invalid username or password.")

#     return render(request, "donors/donor_login.html")

# @login_required(login_url='donor_login')
# def donor_dashboard(request):
#     try:
#         donor_profile = Donor.objects.get(username=request.user.username)  # ✅ Fetch the actual donor object
#     except Donor.DoesNotExist:
#         return render(request, "error.html", {"message": "User profile not found"})

#     return render(request, "donors/donor_dashboard.html", {"donor_profile": donor_profile})

# # Leaderboard
# def leaderboard(request):
#     top_donors = Donor.objects.order_by('-donation_count')[:10]  # ✅ Ensure this field exists
#     return render(request, "donors/leaderboard.html", {'top_donors': top_donors})

# @login_required(login_url='donor_login')

# @login_required(login_url='donor_login')
# def donor_profile(request):
#     donor = Donor.objects.get(username=request.user.username)  # ✅ Fetch donor instance
    
#     # ✅ Ensure profile_picture exists before using it
#     profile_picture_url = donor.profile_picture.url if donor.profile_picture else None  

#     return render(request, "donors/profile.html", {"donor": donor, "profile_picture_url": profile_picture_url})



# @login_required(login_url='donor_login')
# def schedule_donation(request):
#     return render(request, "donors/schedule.html")

# @login_required(login_url='donor_login')
# def my_impact(request):
#     donor, created = Donor.objects.get_or_create(
#         username=request.user.username,
#         defaults={
#             "email": request.user.email,
#             "full_name": request.user.get_full_name() or request.user.username,
#             "mobile_number": "1234567890",  # Placeholder (update accordingly)
#             "dob": "2000-01-01",  # ✅ Provide a default dob to prevent IntegrityError
#         },
#     )

#     return render(request, "donors/impact.html", {"donor": donor})


# @login_required(login_url='donor_login')
# def resources(request):
#     return render(request, "donors/resources.html")

# @login_required(login_url='donor_login')
# def community(request):
#     return render(request, "donors/community.html")

# @login_required(login_url='donor_login')
# def faq(request):
#     return render(request, "donors/faq.html")



# def logout_view(request):
#     messages.success(request, "You have been logged out successfully.")  # Add a success message
#     logout(request)
#     return redirect('donor_login')  # Redirect to login page


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_otp_to_email, otp_store
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from .models import Donor
from .forms import DonorRegistrationForm
from .decorators import donor_login_required
import pdb
import logging


logger = logging.getLogger(__name__)

def email_authenticate(email, password):
    try:
        user = Donor.objects.get(email=email)
        if user.check_password(password):
            return user
    except Donor.DoesNotExist:
        return None
    return None

def donor_register(request):
    if request.method == "POST":
        form = DonorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                donor = form.save(commit=False)
                raw_password = form.cleaned_data.get("password")
                donor.set_password(raw_password)
                donor.date_joined = now()
                donor.donation_count = donor.donation_count or 0
                donor.save()
                request.session['donor_id'] = donor.id
                messages.success(request, "Registration successful!")
                return redirect("donor_dashboard")
            except Exception as e:
                logger.error(f"Registration error: {e}")
                messages.error(request, "Something went wrong. Try again.")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = DonorRegistrationForm()
    return render(request, "donors/donor_register.html", {"form": form})


def donor_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            donor = Donor.objects.get(email=email)
            if donor.check_password(password):
                request.session['donor_id'] = donor.id
                return redirect("donor_dashboard")
            else:
                messages.error(request, "Invalid email or password.")
        except Donor.DoesNotExist:
            messages.error(request, "Donor does not exist.")
    return render(request, "donors/donor_login.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("donor_login")


@donor_login_required
# def donor_dashboard(request):
#     if 'donor_id' not in request.session:
#         return redirect('donor_login')  # Redirect to login if not authenticated
    
#     # Retrieve the donor's data from the session
#     donor_id = request.session['donor_id']
#     donor = Donor.objects.get(id=donor_id)
    
#     # Prepare dashboard widgets or other context data
#     widgets = [
#         {"title": "Upcoming Donations", "icon": "fas fa-calendar-alt", "data": ["Upcoming blood drive: May 5, 2025"]},
#         {"title": "My Blood Donations", "icon": "fas fa-tint", "data": ["Donation on March 20, 2025", "Donation on January 15, 2025"]},
#     ]

#     overview = "Here you can track your donations, schedule new ones, and see your impact!"

#     return render(request, "donors/donor_dashboard.html", {
#         "donor": donor,
#         "widgets": widgets,
#         "overview": overview,
#     })

def donor_dashboard(request):
    if 'donor_id' not in request.session:
        return redirect('donor_login')  # Redirect to login if not authenticated

    donor_id = request.session['donor_id']
    donor = Donor.objects.get(id=donor_id)

    # Widgets Data
    widgets = [
        {
            "title": "Personal Information",
            "icon": "fas fa-user-circle",
            "data": [
                f"Name: {donor.full_name}",
                f"Gender: {dict(Donor.GENDER_CHOICES).get(donor.gender)}",
                f"Date of Birth: {donor.dob.strftime('%d %b %Y')}",
                f"Email: {donor.email}",
                f"Phone: {donor.mobile_number}",
            ]
        },
        {
            "title": "Blood Information",
            "icon": "fas fa-tint",
            "data": [
                f"Blood Group: {donor.blood_group}",
                f"Last Donation Date: {donor.last_donation_date if donor.last_donation_date else 'Not Donated Yet'}",
                f"Total Donations: {donor.donation_count}",
                f"Thalassemia Status: {'Positive' if donor.thalassemia_status else 'Negative'}",
            ]
        },
        {
            "title": "Location Information",
            "icon": "fas fa-map-marker-alt",
            "data": [
                f"Address: {donor.house_number}, {donor.street}, {donor.zip_code}",
                f"Location: {donor.latitude}, {donor.longitude}" if donor.latitude and donor.longitude else "Location not set",
            ]
        },
        {
            "title": "Profile & Settings",
            "icon": "fas fa-cogs",
            "data": [
                f"Profile Picture: {donor.profile_picture.url if donor.profile_picture else 'No profile picture'}",
                "Update your settings and preferences",
            ]
        }
    ]

    # Overview Text
    overview = "Here you can track your donations, schedule new ones, and see your impact!"

    return render(request, "donors/donor_dashboard.html", {
        "donor": donor,
        "widgets": widgets,
        "overview": overview,
    })
    
@donor_login_required
def donor_profile(request):
    donor = Donor.objects.get(id=request.session.get('donor_id'))
    profile_picture_url = donor.profile_picture.url if donor.profile_picture else None
    return render(request, "donors/profile.html", {"donor": donor, "profile_picture_url": profile_picture_url})


@donor_login_required
def my_impact(request):
    donor_id = request.session.get('donor_id')
    if donor_id:
        try:
            donor = Donor.objects.get(id=donor_id)
            # Assuming a function get_total_donations exists on the Donor model or related models
            donation_count = donor.donation_count  # Or get from related models
            lives_saved = donation_count * 3  # Approximate lives saved based on donations
        except Donor.DoesNotExist:
            donor = None
            donation_count = 0
            lives_saved = 0
    else:
        donor = None
        donation_count = 0
        lives_saved = 0

    return render(request, 'donors/impact.html', {
        'donor': donor,
        'donation_count': donation_count,
        'lives_saved': lives_saved,
    })


@donor_login_required
def leaderboard(request):
    top_donors = Donor.objects.order_by('-donation_count')[:10]
    return render(request, "donors/leaderboard.html", {'top_donors': top_donors})


@donor_login_required
def schedule_donation(request):
    return render(request, "donors/schedule.html")


@donor_login_required
def resources(request):
    return render(request, "donors/resources.html")


@donor_login_required
def community(request):
    return render(request, "donors/community.html")


@donor_login_required
def faq(request):
    return render(request, "donors/faq.html")

@csrf_exempt
def send_otp_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        if email:
            send_otp_to_email(email)
            return JsonResponse({"message": "OTP sent successfully!"})
        return JsonResponse({"message": "Email is required."}, status=400)
    return JsonResponse({"message": "Invalid request."}, status=400)

@csrf_exempt
def verify_otp_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        otp = data.get("otp")
        if email and otp:
            if otp_store.get(email) == otp:
                del otp_store[email]  # Clear after success
                return JsonResponse({"message": "OTP verified!", "verified": True})
            return JsonResponse({"message": "Invalid OTP!", "verified": False})
        return JsonResponse({"message": "Email and OTP are required."}, status=400)
    return JsonResponse({"message": "Invalid request."}, status=400)

@donor_login_required
def change_donor_password(request):
    donor_id = request.session.get('donor_id')
    donor = get_object_or_404(Donor, id=donor_id)

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not donor.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            donor.set_password(new_password)
            donor.save()
            messages.success(request, "Password updated successfully!")
            return redirect('donor_profile')  # adjust to your actual profile URL name

    return render(request, "donors/change_password.html", {"donor": donor})
@csrf_exempt
def reset_donor_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        new_password = data.get("new_password")

        if not email or not new_password:
            return JsonResponse({"message": "Missing data", "success": False}, status=400)

        try:
            donor = Donor.objects.get(email=email)
            donor.set_password(new_password)
            donor.save()
            return JsonResponse({"message": "Password reset successful!", "success": True})
        except Donor.DoesNotExist:
            return JsonResponse({"message": "Donor not found.", "success": False}, status=404)

    return JsonResponse({"message": "Invalid request"}, status=400)
def forgot_password_page(request):
    return render(request, "donors/forgot_password.html")
