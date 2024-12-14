# CMG109D5

import sys
from django.utils import timezone

sys.path.insert(0, '../../')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ujurbackend.settings')
import django
django.setup()

from doctors.models import Appointment, DoctorLeave, doctorDetails

today = timezone.now().date()

# Make inactive if leave is approved and from_date is today
doctors_to_change = doctorDetails.objects.filter(
    ujur_id__startswith="CMG109",
)
for doctor in doctors_to_change:
    doctor.education = " "
    doctor.save()
