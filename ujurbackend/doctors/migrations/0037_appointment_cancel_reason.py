# Generated by Django 5.0.2 on 2024-06-22 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0036_appointment_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='cancel_reason',
            field=models.TextField(null=True),
        ),
    ]