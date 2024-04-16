import datetime
from django.db import models
from django.utils import timezone

from patients.models import Patient
from users.models import UsersDetails
from django.core.validators import FileExtensionValidator


class HospitalDetails(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='hospital_logos/', blank=True, null=True)

    class Meta:
        managed = True
        db_table = "hospital_details"


class HospitalAdmin(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "hospital_admin"


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        managed = True
        db_table = "department"


class DepartmentHospitalMapping(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "hospital_department_mapping"


class LabReports(models.Model):
    Patients = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE)
    report = models.FileField(upload_to='hospital_reports/', validators=[FileExtensionValidator(['pdf'])], blank=True,
                              null=True)
    report_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "lab_reports_hospital"


class MedicinesName(models.Model):
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        managed = True
        db_table = "medicines_name"


class ReferToDoctors(models.Model):
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = "refer_to"
