# bloodbank/models.py
from django.db import models

class BloodBank(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name



    

