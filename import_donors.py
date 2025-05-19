import os
import django
import csv
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "raktkan.settings")
django.setup()

from donors.models import Donor  # Adjust if your app name is different

with open('donors_indore.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        donor = Donor(
            email=row['email'],
            full_name=row['full_name'],
            dob=row['dob'],
            gender=row['gender'],
            mobile_number=row['mobile_number'],
            alternate_contact=row['alternate_contact'] if row['alternate_contact'] else None,
            share_contact=row['share_contact'] == 'True',
            blood_group=row['blood_group'],
            last_donation_date=row['last_donation_date'] if row['last_donation_date'] else None,
            thalassemia_status=row['thalassemia_status'] == 'True',
            donation_count=int(row['donation_count']),
            city=row['city'],
            house_number=row['house_number'],
            street=row['street'],
            zip_code=row['zip_code'],
            latitude=float(row['latitude']) if row['latitude'] else None,
            longitude=float(row['longitude']) if row['longitude'] else None,
            date_joined=datetime.strptime(row['date_joined'], "%Y-%m-%d %H:%M:%S")
        )
        donor.set_password(row['password'])  # Set hashed password properly
        donor.save()

print("Donors imported successfully.")
