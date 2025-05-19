from django import forms
from .models import DonationDrive

class DonationDriveForm(forms.ModelForm):
    class Meta:
        model = DonationDrive
        fields = ['title', 'description', 'start_date','end_date', 'start_time','end_time', 'location', 'organizer_name', 'contact_info', 'poster' ] 
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
             'description': forms.Textarea(attrs={
                'rows': 5,  # You can adjust the height by changing rows
                'class': 'form-control',
                'placeholder': 'Enter a detailed description of the donation drive...',
                 }),
        }
        
