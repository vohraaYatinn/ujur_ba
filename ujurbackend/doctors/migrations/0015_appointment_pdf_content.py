# Generated by Django 5.0.2 on 2024-03-03 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0014_doctorslots_medical_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='pdf_content',
            field=models.TextField(null=True),
        ),
    ]
