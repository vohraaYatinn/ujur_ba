# Generated by Django 5.0.2 on 2024-02-13 09:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_initial'),
        ('hospitals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='date_booked',
        ),
        migrations.AddField(
            model_name='appointment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='slot',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='doctordetails',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_doctors', to='hospitals.hospitaldetails'),
        ),
    ]
