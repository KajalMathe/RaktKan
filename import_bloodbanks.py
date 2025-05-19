import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "raktkan.settings")
django.setup()

from bloodbanks.models import BloodBank

with open('indore_bloodbank.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        BloodBank.objects.create(
            name=row['name'],
            address=row['address'],
            latitude=float(row['latitude']),
            longitude=float(row['longitude']),
            phone=row['phone'],
            email=row['email']
        )

print("Blood banks imported successfully.")
