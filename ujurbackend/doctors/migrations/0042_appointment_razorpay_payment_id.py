# Generated by Django 5.0.2 on 2024-06-25 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0041_revenue_doctor_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='razorpay_payment_id',
            field=models.TextField(null=True),
        ),
    ]
