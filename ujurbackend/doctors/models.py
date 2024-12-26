from django.db import models
from django.utils import timezone
from hospitals.models import HospitalDetails, Department
from patients.models import Patient
from users.models import UsersDetails


class doctorDetails(models.Model):
    ujur_id = models.CharField(max_length=15, unique=True, null=True)
    user = models.OneToOneField(UsersDetails, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    specialization = models.CharField(max_length=100, null=True)
    experience = models.PositiveIntegerField()
    education = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    signature = models.ImageField(upload_to='doctor_sign/', blank=True, null=True)
    prescription_mode = models.CharField(max_length=200, null=True, default="digital")
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE, related_name="hospital_doctors")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "doctor_details"


class doctorSlots(models.Model):
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE, related_name="doctor_slots")
    medical_license = models.CharField(max_length=200,null=True)
    morning_timings = models.CharField(max_length=200, null=True)
    afternoon_timings = models.CharField(max_length=200, null=True)
    evening_timings = models.CharField(max_length=200, null=True)
    morning_slots = models.PositiveIntegerField(null=True)
    afternoon_slots = models.PositiveIntegerField(null=True)
    evening_slots = models.PositiveIntegerField(null=True)
    morning_slots_price = models.PositiveIntegerField(null=True)
    afternoon_slots_price = models.PositiveIntegerField(null=True)
    evening_slots_price = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "doctor_slots"


# payment created when not payment not dene
# payment pending when payment done
# payment past when completed
# payment missed when not present there
# appointment canceled present there
# appointment completed present there
# queue completed present there


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE, related_name='doctor')
    appointment_slot = models.CharField(max_length=100, null=True)
    patient_documents = models.FileField(upload_to='patient_documents/', null=True, blank=True)
    slot = models.CharField(max_length=100)
    date_appointment = models.DateTimeField()
    status = models.CharField(max_length=100, default="created")
    prescription_method = models.CharField(max_length=100, default="digital")
    payment_mode = models.CharField(max_length=100, null=True)
    payment_status = models.CharField(max_length=100, null=True)
    patients_query = models.TextField(null=True)
    doctor_instruction = models.TextField(null=True)
    pdf_content = models.TextField(null=True)
    cancel_reason = models.TextField(null=True)
    razorpay_payment_id = models.TextField(null=True)
    lab_report = models.FileField(upload_to='lab_report/', blank=True, null=True)
    prescription = models.FileField(upload_to='prescription/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'slot', 'date_appointment', 'appointment_slot'],
                name='unique_appointment_per_doctor_slot'
            )
        ]
        managed = True
        db_table = "appointment"



class Revenue(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='revenues')
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2)
    doctor_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "revenue"


class FavDoctors(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "fav_doctor"


class PatientDoctorReviews(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_reviews")
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE,  related_name="doctor_reviews")
    reviews_star = models.IntegerField()
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "patient_doctor_reviews"

class HospitalPatientReviews(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_hospital", null=True)
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE,  related_name="hospital_reviews", null=True)
    reviews_star = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        managed = True
        db_table = "hospital_doctor_reviews"



# APPLIED
# APPROVED
# REJECTED
class DoctorLeave(models.Model):
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE,  related_name="doctor_apply")
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=200, null=True, default="Waiting for approval")
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "doctor_leave"

# REQUESTED
# CANCELLED
# APPROVED
class ResetPasswordRequest(models.Model):
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE, related_name="reset_password_doctor")
    comment = models.TextField()
    status = models.CharField(max_length=200, null=True, default="REQUESTED")

    class Meta:
        managed = True
        db_table = "reset_password"

class getChiefQuery(models.Model):
    value = models.CharField(max_length=200, null=True)
    label = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "get_chief_query"

class labTests(models.Model):
    value = models.CharField(max_length=200, null=True)
    label = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "lab_tests"
