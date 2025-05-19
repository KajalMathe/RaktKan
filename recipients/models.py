from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Recipient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    URGENCY_CHOICES = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Critical', 'Critical'),
    ]

    # Login Credentials
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Personal Details
    full_name = models.CharField(max_length=100,null=True)
    mobile_number = models.CharField(max_length=15, unique=True,null=True)

    # Blood Request Details
    reason_for_request = models.TextField(blank=True, null=True)
    blood_group_needed = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    blood_units_required = models.PositiveIntegerField(default=1, null=True, blank=True)

    # Hospital Info
    hospital_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    # medical_condition = models.TextField(blank=True, null=True)

    # Location Details (Auto capture)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Profile
    # profile_picture = models.ImageField(upload_to="recipient_profiles/", blank=True, null=True)

    # Meta Information
    request_date = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.full_name or "Unnamed Recipient"
