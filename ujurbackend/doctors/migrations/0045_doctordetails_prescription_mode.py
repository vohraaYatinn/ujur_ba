# Generated by Django 5.0.2 on 2024-08-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0044_appointment_prescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctordetails',
            name='prescription_mode',
            field=models.CharField(default='digital', max_length=200, null=True),
        ),
    ]