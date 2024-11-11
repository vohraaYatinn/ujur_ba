import sys
from django.utils import timezone

sys.path.insert(0, '../../')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ujurbackend.settings')
import django
django.setup()

from doctors.models import Appointment, DoctorLeave

today = timezone.now().date()

# Make inactive if leave is approved and from_date is today
leaves_to_start = DoctorLeave.objects.filter(
    status="APPROVED",
    from_date=today
)
for leave in leaves_to_start:
    leave.doctor.is_active = False
    leave.doctor.save()

# Make active if leave is approved, doctor is inactive, and to_date was yesterday
yesterday = today - timezone.timedelta(days=1)
leaves_to_end = DoctorLeave.objects.filter(
    status="APPROVED",
    to_date=yesterday,
    doctor__is_active=False
)
print(leaves_to_end)
for leave in leaves_to_end:
    leave.doctor.is_active = True
    leave.doctor.save()

active_leaves = DoctorLeave.objects.filter(
    status="APPROVED",
    from_date__lte=today
)
for leave in active_leaves:
    appointments_to_cancel = Appointment.objects.filter(
        doctor=leave.doctor,
        date_appointment__date__range=(leave.from_date, leave.to_date),
        status="pending"
    )
    for appointment in appointments_to_cancel:
        appointment.status = "canceled"
        appointment.cancel_reason = "doctor is on leave"
        appointment.save()