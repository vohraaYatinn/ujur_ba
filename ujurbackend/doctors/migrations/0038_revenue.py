# Generated by Django 5.0.2 on 2024-06-24 05:44

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0037_appointment_cancel_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenues', to='doctors.appointment')),
            ],
            options={
                'db_table': 'revenue',
                'managed': True,
            },
        ),
    ]