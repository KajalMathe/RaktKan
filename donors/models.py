# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class Donor(AbstractUser):  # Extend AbstractUser properly
#     GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
#     BLOOD_GROUPS = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
#                     ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')]
#     # PREFERRED_LOCATIONS = [('Hospital', 'Hospital'), ('Blood Bank', 'Blood Bank'), ('Home Pickup', 'Home Pickup')]
#     # CONTACT_TIMES = [('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening')]

#     # Override groups and permissions to avoid conflicts
#     groups = models.ManyToManyField(
#         "auth.Group",
#         related_name="donor_users",
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission",
#         related_name="donor_users",
#         blank=True
#     )

#     # Personal Information
#     full_name = models.CharField(max_length=100)
#     dob = models.DateField()
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

#     # Contact Information
#     mobile_number = models.CharField(max_length=15, unique=True, blank=False)
#     alternate_contact = models.CharField(max_length=15, blank=True, null=True)
#     share_contact = models.BooleanField(default=False)

#     # Blood Information
#     blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
#     last_donation_date = models.DateField(blank=True, null=True)
#     thalassemia_status = models.BooleanField(default=False)
#     donation_count = models.PositiveIntegerField(default=0)  # ✅ Default 0
#     date_joined = models.DateTimeField(auto_now_add=True)  # ✅ Auto-set on creation

#     # Address & Location
#     house_number = models.CharField(max_length=50)
#     street = models.CharField(max_length=100)
#     # city = models.CharField(max_length=50)
#     # state = models.CharField(max_length=50)
#     zip_code = models.CharField(max_length=10)
#     # country = models.CharField(max_length=50, default="India")
#     latitude = models.FloatField(blank=True, null=True)
#     longitude = models.FloatField(blank=True, null=True)

#     # Availability & Preferences
#     # willing_to_donate = models.BooleanField(default=True)
#     # preferred_location = models.CharField(max_length=20, choices=PREFERRED_LOCATIONS, blank=True, null=True)
#     # preferred_time = models.CharField(max_length=10, choices=CONTACT_TIMES, blank=True, null=True)
#     # can_donate_for_thalassemia = models.BooleanField(default=False)

#     # Additional Information
#     profile_picture = models.ImageField(upload_to="donor_profiles/", blank=True, null=True)
#     # id_proof = models.FileField(upload_to="donor_ids/", blank=True, null=True)
#     # health_conditions = models.TextField(blank=True, null=True)
#     # remarks = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.full_name  # ✅ Moved this to the correct place



# donors/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Donor(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    BLOOD_GROUPS = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                    ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')]

    # Basic Auth Fields
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Personal Information
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    # Contact Information
    mobile_number = models.CharField(max_length=15, unique=True, blank=False)
    alternate_contact = models.CharField(max_length=15, blank=True, null=True)
    share_contact = models.BooleanField(default=False)

    # Blood Information
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    last_donation_date = models.DateField(blank=True, null=True)
    thalassemia_status = models.BooleanField(default=False)
    donation_count = models.PositiveIntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Address & Location
    city = models.CharField(max_length=100 ,blank=True,null=True,default='Indore')
    house_number = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Additional
    profile_picture = models.ImageField(upload_to="donor_profiles/", blank=True, null=True)

    # Custom methods
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.full_name
