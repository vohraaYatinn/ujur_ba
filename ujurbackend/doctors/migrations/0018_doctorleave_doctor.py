# Generated by Django 5.0.2 on 2024-03-04 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0017_alter_doctorleave_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorleave',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_apply', to='doctors.doctordetails'),
            preserve_default=False,
        ),
    ]
