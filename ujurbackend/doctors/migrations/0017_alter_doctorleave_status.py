# Generated by Django 5.0.2 on 2024-03-04 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0016_doctorleave_doctordetails_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorleave',
            name='status',
            field=models.CharField(default='APPLIED', max_length=200, null=True),
        ),
    ]
