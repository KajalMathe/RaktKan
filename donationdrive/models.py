from django.db import models
from django.utils import timezone

class DonationDrive(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # 🗓️ Start and End Date/Time
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    location = models.CharField(max_length=255)
    organizer_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=100)
    
    approved = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='donation_posters/', blank=True, null=True)

    def is_upcoming(self):
        return self.end_date >= timezone.now().date()

    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.end_date})"
