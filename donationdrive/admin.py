from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django import forms
from .models import DonationDrive

# Custom form with widgets for better admin UI
class DonationDriveForm(forms.ModelForm):
    class Meta:
        model = DonationDrive
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
# Registering with custom form
@admin.register(DonationDrive)
class DonationDriveAdmin(admin.ModelAdmin):
    form = DonationDriveForm  # ✅ connect custom form here
    list_display = ('title', 'start_date', 'end_date', 'location', 'approved')
    list_filter = ('approved', 'start_date')
    search_fields = ('title', 'organizer_name', 'location')
