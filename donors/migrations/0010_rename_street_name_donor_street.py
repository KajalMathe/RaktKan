# Generated by Django 5.1.3 on 2025-03-29 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0009_alter_donor_donation_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donor',
            old_name='street_name',
            new_name='street',
        ),
    ]
