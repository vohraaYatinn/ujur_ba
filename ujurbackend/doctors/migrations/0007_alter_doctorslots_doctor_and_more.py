# Generated by Django 5.0.2 on 2024-02-15 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0006_doctorslots_afternoon_slots_price_and_more'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorslots',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_slots', to='doctors.doctordetails'),
        ),
        migrations.AlterField(
            model_name='patientdoctorreviews',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_reviews', to='doctors.doctordetails'),
        ),
        migrations.AlterField(
            model_name='patientdoctorreviews',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_reviews', to='patients.patient'),
        ),
    ]
