# Generated by Django 5.0.2 on 2024-05-30 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0009_alter_patient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_who_created_created_by', to='patients.patient'),
        ),
    ]