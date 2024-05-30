import datetime
from django.db import models
from django.utils import timezone
from users.models import UsersDetails


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    profile_picture = models.ImageField(upload_to='patient/', blank=True, null=True)
    ujur_id = models.CharField(max_length=200, null=True)
    full_name = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(UsersDetails, on_delete=models.CASCADE, related_name="user_patient_table")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text='Weight in kilograms', null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text='Weight in Foots', null=True)
    address = models.TextField()
    district = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name='patient_who_created_created_by', blank=True)


    class Meta:
        managed = True
        db_table = "patient_details"

