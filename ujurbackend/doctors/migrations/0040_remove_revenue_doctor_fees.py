# Generated by Django 5.0.2 on 2024-06-24 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0039_revenue_doctor_fees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revenue',
            name='doctor_fees',
        ),
    ]
