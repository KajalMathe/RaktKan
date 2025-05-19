# admins/models.py
from django.db import models

class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name
