# Generated by Django 5.0.2 on 2024-05-27 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0014_alter_medicinesname_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaladmin',
            name='ujur_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]