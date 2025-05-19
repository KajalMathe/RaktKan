# # recipient/views.py
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# from .models import RecipientProfile
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required


# def recipient_register(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         blood_needed = request.POST["blood_needed"]
#         city = request.POST["city"]
#         urgency = request.POST.get("urgency", "")
        
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists!")
#         else:
#             user = User.objects.create_user(username=username, password=password)
#             RecipientProfile.objects.create(user=user, blood_needed=blood_needed, city=city, urgency=urgency)
#             messages.success(request, "Registration successful!")
#             return redirect("recipients/recipient_login")
#     return render(request, "recipients/recipient_register.html")

# def recipient_login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("recipient_dashboard")  # Redirect to recipient dashboard
#         else:
#             messages.error(request, "Invalid username or password.")

#     return render(request, "recipients/recipient_login.html")

# @login_required(login_url='recipient_login')
# def recipient_dashboard(request):
#     return render(request, "recipients/recipient_dashboard.html")
# from django.contrib.auth import logout
# from django.shortcuts import redirect

# def logout_view(request):
#     logout(request)
#     return redirect('recipient_login')  # or 'home'


# from django.shortcuts import render
# from donors.models import Donor  # Assuming Donor model exists in the same app
# @login_required
# def find_donors(request):
#     location = request.GET.get('location', '')
#     blood_group = request.GET.get('blood_type', '')

#     # Update to match the actual fields (street, zip_code, latitude, longitude)
#     donors = Donor.objects.filter(
#         street__icontains=location,
#         zip_code__icontains=location,
#         blood_group=blood_group
#     )

#     return render(request, 'recipients/find_donors.html', {'donors': donors})


# @login_required
# def your_request(request):
#     # Later you can fetch the recipient’s requests from the DB
#     # For now, we'll just render a page
#     return render(request, 'recipients/your_request.html')
from django.shortcuts import render, redirect
from .forms import BloodRequestForm
from .models import Recipient
from .decorators import recipient_login_required

from django.shortcuts import render, redirect
from .models import Recipient
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from .models import Recipient
from .decorators import recipient_login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recipient
from .forms import RecipientRegistrationForm , RecipientEditForm
from .decorators import recipient_login_required
import logging
from donors.models import Donor

logger = logging.getLogger(__name__)

def recipient_register(request):
    if request.method == "POST":
        form = RecipientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                recipient = form.save(commit=False)
                raw_password = form.cleaned_data.get("password")

                recipient.set_password(raw_password)
                recipient.save()
                request.session['recipient_id'] = recipient.id
                messages.success(request, "Registration successful!")
                return redirect("recipient_dashboard")
            except Exception as e:
                logger.error(f"Registration error: {e}")
                messages.error(request, "Something went wrong. Try again.")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RecipientRegistrationForm()
    return render(request, "recipients/recipient_register.html", {"form": form})


def recipient_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            recipient = Recipient.objects.get(email=email)
            if recipient.check_password(password):
                request.session['recipient_id'] = recipient.id
                return redirect("recipient_dashboard")
            else:
                messages.error(request, "Invalid email or password.")
        except Recipient.DoesNotExist:
            messages.error(request, "Recipient does not exist.")
    return render(request, "recipients/recipient_login.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("recipient_login")


@recipient_login_required
def recipient_dashboard(request):
    recipient = Recipient.objects.get(id=request.session.get('recipient_id'))
    return render(request, "recipients/recipient_dashboard.html", {"recipient": recipient})


@recipient_login_required
def recipient_profile(request):
    recipient = Recipient.objects.get(id=request.session.get('recipient_id'))
    profile_picture_url = recipient.profile_picture.url if recipient.profile_picture else None
    return render(request, "recipients/profile.html", {"recipient": recipient, "profile_picture_url": profile_picture_url})


@recipient_login_required
def find_blood_banks(request):
    return render(request, "recipients/find_blood_banks.html")

from donors.models import Donor
from geopy.distance import geodesic
from django.http import Http404
@recipient_login_required  # Ensure only logged-in recipients can access this view
def find_donors(request):
    try:
        # Fetch the recipient using the session data
        recipient = Recipient.objects.get(id=request.session['recipient_id'])
    except Recipient.DoesNotExist:
        raise Http404("Recipient not found")

    # Get all donors initially
    donors = Donor.objects.all()

    # Get recipient's required blood group
    required_blood_group = recipient.blood_group_needed

    # Filter donors by blood group
    donors = donors.filter(blood_group=required_blood_group)

    # If a location is provided (latitude and longitude), filter donors by proximity
    if recipient.latitude and recipient.longitude:
        recipient_coords = (recipient.latitude, recipient.longitude)  # Recipient's coordinates
        donors_nearby = []

        for donor in donors:
            if donor.latitude and donor.longitude:
                donor_coords = (donor.latitude, donor.longitude)
                distance = geodesic(recipient_coords, donor_coords).km
                if distance <= 50:  # Donors within 50 km radius
                    donors_nearby.append(donor)

        donors = donors_nearby  # Update the donor list to only include those within 50 km radius

    return render(request, 'recipients/find_donors.html', {
        'donors': donors, 
        'required_blood_group': required_blood_group
    })


@recipient_login_required
def your_request(request):
    recipient_id = request.session.get('recipient_id')

    # If no recipient is found in the session, redirect to login
    if not recipient_id:
        messages.error(request, "You need to be logged in to view your requests.")
        return redirect('recipient_login')

    try:
        # Fetch the recipient details
        recipient = Recipient.objects.get(id=recipient_id)
    except Recipient.DoesNotExist:
        messages.error(request, "Recipient not found.")
        return redirect('recipient_login')  # fallback if recipient doesn't exist

    # Check if the recipient has an active request
    if recipient.reason_for_request:  # This is where we check if a request exists
        # If a request exists, pass it to the template
        requests = [recipient]  # Wrap recipient in a list for template rendering
    else:
        requests = []  # No active requests, empty list

    return render(request, 'recipients/your_request.html', {'requests': requests})


    

@recipient_login_required
def recipient_logout(request):
    if 'recipient_email' in request.session:
        del request.session['recipient_email']
    return redirect('recipient_login')  # or wherever you want to send them after logout


@recipient_login_required
def create_blood_request(request):
    recipient_id = request.session.get('recipient_id')

    if not recipient_id:
        return redirect('recipient_login')

    recipient = Recipient.objects.get(id=recipient_id)

    # ✅ Check if user already has a blood request
    if Recipient.objects.filter(email=recipient.email, reason_for_request__isnull=False).exists():
        messages.error(request, "You already have an active blood request.")
        

    if request.method == "POST":
        recipient.reason_for_request = request.POST.get("reason_for_request")
        recipient.emergency = request.POST.get("emergency") == "True"
        recipient.hospital_name = request.POST.get("hospital_name")
        recipient.location = request.POST.get("location")
        recipient.blood_group_needed = request.POST.get("blood_group_needed")
        recipient.units_required = request.POST.get("units_required")
        recipient.save()

        messages.success(request, "Your blood request has been created successfully!")

    return render(request, "recipients/create_blood_request.html", {"recipient": recipient})

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def cancel_blood_request(request):
    recipient_id = request.session.get("recipient_id")
    if not recipient_id:
        return redirect("recipient_login")

    recipient = get_object_or_404(Recipient, id=recipient_id)

    # Clear only request-related fields
    recipient.reason_for_request = None
    recipient.emergency = False
    recipient.hospital_name = None
    recipient.location = None
    recipient.blood_group_needed = None
    recipient.units_required = None
    recipient.save()

    messages.success(request, "Your blood request has been cancelled.")
    return redirect("your_request")

@recipient_login_required
def recipient_profile(request):
    recipient_id = request.session.get('recipient_id')
    recipient = get_object_or_404(Recipient, id=recipient_id)
    return render(request, "recipients/profile.html", {"recipient": recipient})

@recipient_login_required
def edit_recipient_profile(request):
    recipient_id = request.session.get('recipient_id')
    recipient = get_object_or_404(Recipient, id=recipient_id)

    if request.method == "POST":
        form = RecipientEditForm(request.POST, request.FILES, instance=recipient)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('recipient_profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RecipientEditForm(instance=recipient)

    return render(request, "recipients/edit_profile.html", {"form": form, "recipient": recipient})

@recipient_login_required
def change_recipient_password(request):
    recipient_id = request.session.get('recipient_id')
    recipient = get_object_or_404(Recipient, id=recipient_id)

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not recipient.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            recipient.set_password(new_password)
            recipient.save()
            messages.success(request, "Password updated successfully!")
            return redirect('recipient_profile')

    return render(request, "recipients/change_password.html", {"recipient": recipient})