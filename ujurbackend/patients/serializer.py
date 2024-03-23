from rest_framework import serializers
from doctors.models import Appointment
from doctors.serializer import DoctorHospitalSerializer
from patients.models import Patient
from users.serializer import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorHospitalSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"


class PatientDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Patient
        fields = "__all__"
