# Generated by Django 5.0.2 on 2024-08-20 11:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0017_hospitaldetails_years_of_establishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
