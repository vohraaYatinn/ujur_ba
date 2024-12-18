# Generated by Django 5.0.2 on 2024-02-12 03:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='otpPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'otp_phone',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UsersDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=50, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('role', models.CharField(default='doctor', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'user_table',
                'managed': True,
            },
        ),
    ]
