from django import forms
from .models import Recipient
class RecipientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Recipient
        fields = [
            'full_name',
            'email',
            'password',
            'confirm_password',
            'mobile_number',
            'blood_group_needed',
            'urgency',
            'blood_units_required',
            'hospital_name',
            'location',
            'latitude',
            'longitude',
        ]
        widgets = {
            'blood_group_needed': forms.Select(choices=Recipient.BLOOD_GROUP_CHOICES),
            'urgency': forms.Select(choices=Recipient.URGENCY_CHOICES),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")



class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = [
            'blood_group_needed', 'blood_units_required', 'urgency',
            'hospital_name', 'location', 'reason_for_request'
        ]
        widgets = {
            'reason_for_request': forms.Textarea(attrs={'rows': 3}),
            'blood_group_needed': forms.Select(choices=Recipient.BLOOD_GROUP_CHOICES),
            'urgency': forms.Select(choices=Recipient.URGENCY_CHOICES),
        }


class RecipientEditForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['full_name', 'email', 'mobile_number', 'blood_group_needed']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
