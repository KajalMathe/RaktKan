# from django import forms
# from django.core.exceptions import ValidationError
# from django.utils.timezone import now
# from .models import Donor

# class DonorRegistrationForm(forms.ModelForm):
#     date_joined = forms.DateField(
#         widget=forms.HiddenInput(),
#         initial=now().date()
#     )

#     dob = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         required=True,
#         help_text="Select a valid date."
#     )

#     mobile_number = forms.CharField(
#         max_length=10,
#         min_length=10,
#         required=True,
#         widget=forms.TextInput(attrs={
#             'pattern': r'\d{10}',
#             'title': 'Enter a 10-digit mobile number',
#             'placeholder': 'e.g. 0000000000'
#         }),
#         help_text="Enter a 10-digit mobile number."
#     )

#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
#         min_length=8,
#         help_text="Password must be at least 8 characters."
#     )

#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
#         min_length=8,
#         help_text="Re-enter password for confirmation."
#     )

#     class Meta:
#         model = Donor
#         exclude = ['latitude', 'longitude']
#         widgets = {
#             'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#         mobile_number = cleaned_data.get("mobile_number")

#         # Validate password match
#         if password and confirm_password and password != confirm_password:
#             self.add_error("confirm_password", "Passwords do not match.")

#         # Ensure mobile number has only digits
#         if mobile_number and not mobile_number.isdigit():
#             self.add_error("mobile_number", "Mobile number must contain only digits.")

#         return cleaned_data

#     def save(self, commit=True):
#         donor = super().save(commit=False)
#         donor.set_password(self.cleaned_data["password"])  # Securely hash password
#         if commit:
#             donor.save()
#         return donor


from django import forms
from .models import Donor

class DonorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Donor
        fields = [
            'email', 'full_name', 'dob', 'gender', 'mobile_number',
            'alternate_contact', 'share_contact', 'blood_group',
            'last_donation_date', 'thalassemia_status', 'donation_count',
            'house_number', 'street', 'zip_code', 'latitude', 'longitude',
            'profile_picture', 'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password != confirm:
            raise forms.ValidationError("Passwords do not match.")
