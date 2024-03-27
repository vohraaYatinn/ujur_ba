from django.db import models
from django.utils import timezone

class mainAdminDetails(models.Model):
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "admin_details"
