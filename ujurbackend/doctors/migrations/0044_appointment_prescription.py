# Generated by Django 5.0.2 on 2024-08-05 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0043_alter_patientdoctorreviews_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='prescription',
            field=models.FileField(blank=True, null=True, upload_to='prescription/'),
        ),
    ]