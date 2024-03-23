from django.db import models
from django.utils import timezone
from common_constants import CommonConstants


class UsersDetails(models.Model):
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=50, null=True)
    verified = models.BooleanField(default=False)
    role = models.CharField(default=CommonConstants.user_roles['doctor'], max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "user_table"


class otpPhone(models.Model):
    phone_number = models.CharField(max_length=10, null=False)
    otp = models.CharField(max_length=6, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "otp_phone"