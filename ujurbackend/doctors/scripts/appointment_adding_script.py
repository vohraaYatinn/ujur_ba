import sys
sys.path.insert(0, '../../')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ujurbackend.settings')
import django
django.setup()

from doctors.models import Appointment
import datetime
import random

date = datetime.date.today()
for i in range(20):
    check_status = ['completed', "canceled", "pending"]
    random.shuffle(check_status)
    Appointment.objects.create(
        patient_id=1,
        doctor_id=18,
        slot="morning",
        date_appointment=date,
        status=check_status[0],
        payment_mode="payAtHospital",
        patients_query="I am in pain"

    )
for i in range(20):
    check_status = ['completed', "canceled", "pending"]
    random.shuffle(check_status)
    Appointment.objects.create(
        patient_id=1,
        doctor_id=18,
        slot="afternoon",
        date_appointment=date,
        status=check_status[0],
        payment_mode="payAtHospital",
        patients_query="I am in pain"

    )
for i in range(20):
    check_status = ['completed', "canceled", "pending"]
    random.shuffle(check_status)
    Appointment.objects.create(
        patient_id=1,
        doctor_id=18,
        slot="evening",
        date_appointment=date,
        status=check_status[0],
        payment_mode="payAtHospital",
        patients_query="I am in pain"
    )
