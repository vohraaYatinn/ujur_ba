# Generated by Django 5.0.2 on 2024-05-15 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0025_alter_doctordetails_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorslots',
            name='afternoon_timings',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='doctorslots',
            name='evening_timings',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='doctorslots',
            name='morning_timings',
            field=models.CharField(max_length=200, null=True),
        ),
    ]