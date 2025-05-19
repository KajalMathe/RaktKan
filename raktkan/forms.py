from django import forms
from .models import Donor  # or your model name

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }
