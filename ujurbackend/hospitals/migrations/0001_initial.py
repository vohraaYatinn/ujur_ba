# Generated by Django 5.0.2 on 2024-02-12 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'department',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HospitalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(max_length=200)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='hospital_logos/')),
            ],
            options={
                'db_table': 'hospital_details',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HospitalAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.usersdetails')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.hospitaldetails')),
            ],
            options={
                'db_table': 'hospital_admin',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DepartmentHospitalMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.department')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.hospitaldetails')),
            ],
            options={
                'db_table': 'hospital_department_mapping',
                'managed': True,
            },
        ),
    ]
