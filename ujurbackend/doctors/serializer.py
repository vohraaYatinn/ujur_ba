from rest_framework import serializers
from doctors.models import doctorDetails, doctorSlots, PatientDoctorReviews, Appointment, FavDoctors, DoctorLeave, \
    ResetPasswordRequest
from hospitals.models import MedicinesName, ReferToDoctors
from hospitals.serializer import HospitalSerializer, DepartmentSerializer, HospitalDoctorSerializer
from patients.models import Patient
from users.serializer import UserSerializer


class PatientDetailsWithUserDoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Patient
        fields = "__all__"


class PatientDetailsFprDoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"

class DoctorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctorDetails
        fields = "__all__"


class DoctorModelWithDepartmentHospitalSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    hospital = HospitalDoctorSerializer()

    class Meta:
        model = doctorDetails
        fields = "__all__"


class DoctorModelWithDepartmentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = doctorDetails
        fields = "__all__"

class DocotrSlotsSerializer(serializers.ModelSerializer):
    doctor = DoctorModelSerializer()
    class Meta:
        model = doctorSlots
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    avg_reviews = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    doctor_slots = DocotrSlotsSerializer(many=True)
    class Meta:
        model = doctorDetails
        fields = "__all__"


class DoctorReviewsWithPatientsSerializer(serializers.ModelSerializer):
    patient = PatientDetailsFprDoctorSerializer()
    class Meta:
        model = PatientDoctorReviews
        fields = "__all__"


class DoctorAverageUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avg_reviews = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    doctor_slots = DocotrSlotsSerializer(many=True)
    doctor_reviews = DoctorReviewsWithPatientsSerializer(many=True)
    class Meta:
        model = doctorDetails
        fields = "__all__"


class DoctorSingleSerializer(serializers.ModelSerializer):
    avg_reviews = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    user = UserSerializer()
    hospital = HospitalSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = doctorDetails
        fields = "__all__"


class DoctorHospitalSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()
    class Meta:
        model = doctorDetails
        fields = "__all__"


class DoctorReviewsSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    class Meta:
        model = PatientDoctorReviews
        fields = "__all__"


class DoctorSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctorSlots
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorModelSerializer()
    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentWithDepartmentSerializer(serializers.ModelSerializer):
    patient = PatientDetailsFprDoctorSerializer()
    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentWithDepartmentandDoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorModelWithDepartmentSerializer()
    patient = PatientDetailsFprDoctorSerializer()
    class Meta:
        model = Appointment
        fields = "__all__"


class DoctorFavSerializer(serializers.ModelSerializer):
    doctor = DoctorModelWithDepartmentHospitalSerializer()

    class Meta:
        model = FavDoctors
        fields = "__all__"


class AppointmentWithDoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorModelSerializer()
    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentWithDoctorAndPatientSerializer(serializers.ModelSerializer):
    patient = PatientDetailsFprDoctorSerializer()
    doctor = DoctorHospitalSerializer()
    class Meta:
        model = Appointment
        fields = "__all__"




class DoctorUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = doctorDetails
        fields = "__all__"


class PatientAppointmentsSerializer(serializers.ModelSerializer):
    appointments = AppointmentWithDoctorSerializer(many=True)
    class Meta:
        model = Patient
        fields = "__all__"


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLeave
        fields = "__all__"


class LeaveDoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorModelSerializer()
    class Meta:
        model = DoctorLeave
        fields = "__all__"


class resetPasswordsDoctor(serializers.ModelSerializer):
    doctor = DoctorModelSerializer()

    class Meta:
        model = ResetPasswordRequest
        fields = "__all__"


class DoctorReviewsWithPatientsAndDoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorModelWithDepartmentHospitalSerializer()
    patient = PatientDetailsFprDoctorSerializer()
    class Meta:
        model = PatientDoctorReviews
        fields = "__all__"



class DoctorReviewsWithPatientsAndDoctorHospitalSerializer(serializers.ModelSerializer):
    doctor = DoctorModelSerializer(many=True)
    patient = PatientDetailsFprDoctorSerializer()
    class Meta:
        model = PatientDoctorReviews
        fields = "__all__"


class MedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinesName
        fields = "__all__"

class ReferToSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferToDoctors
        fields = "__all__"

class checkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorReviews
        fields = "__all__"
