import sys
import os
import django
from django.utils import timezone
from django.db.models import F
from datetime import datetime
sys.path.insert(0, '.')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ujurbackend.settings')

django.setup()

from doctors.models import Appointment
today = timezone.now().date()

def check_fucntion():
    appointments = Appointment.objects.filter(date_appointment__date=today).order_by('doctor', 'slot', 'created_at')

    # Initialize a dictionary to keep track of the slot counts for each doctor and slot
    slot_counters = {}

    # Iterate through the appointments and update the appointment_slot incrementally
    for appointment in appointments:
        # Create a unique key for each doctor-slot combination
        key = (appointment.doctor_id, appointment.slot)

        # Initialize the counter for this combination if it doesn't exist
        if key not in slot_counters:
            slot_counters[key] = 1
        else:
            slot_counters[key] += 1

        # Update the appointment_slot with the current counter value
        appointment.appointment_slot = slot_counters[key]
        appointment.save()

check_fucntion()