from django.db import models
from django.utils import timezone
from hospitals.models import HospitalDetails, Department
from patients.models import Patient
from users.models import UsersDetails


class doctorDetails(models.Model):
    user = models.OneToOneField(UsersDetails, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    education = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    signature = models.ImageField(upload_to='doctor_sign/', blank=True, null=True)
    hospital = models.ForeignKey(HospitalDetails, on_delete=models.CASCADE, related_name="hospital_doctors")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "doctor_details"


class doctorSlots(models.Model):
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE, related_name="doctor_slots")
    medical_license = models.CharField(max_length=200)
    morning_timings = models.CharField(max_length=200)
    afternoon_timings = models.CharField(max_length=200)
    evening_timings = models.CharField(max_length=200)
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


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE, related_name='doctor')
    slot = models.CharField(max_length=100)
    date_appointment = models.DateTimeField()
    status = models.CharField(max_length=100, default="created")
    payment_mode = models.CharField(max_length=100, null=True)
    patients_query = models.TextField(null=True)
    doctor_instruction = models.TextField(null=True)
    pdf_content = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        managed = True
        db_table = "appointment"


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
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "patient_doctor_reviews"



# APPLIED
# APPROVED
# REJECTED
class DoctorLeave(models.Model):
    doctor = models.ForeignKey(doctorDetails, on_delete=models.CASCADE,  related_name="doctor_apply")
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=200, null=True, default="APPLIED")
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
