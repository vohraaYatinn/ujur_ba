from rest_framework import serializers

from doctors.models import doctorDetails
from hospitals.models import HospitalDetails, Department, LabReports, DepartmentHospitalMapping
from patients.models import Patient



class DoctorModelForHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctorDetails
        fields = "__all__"


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDetails
        fields = "__all__"


class HospitalSerializerWithDoctors(serializers.ModelSerializer):
    hospital_doctors = DoctorModelForHospitalSerializer(many=True)
    class Meta:
        model = HospitalDetails
        fields = "__all__"


class HospitalDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDetails
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class LabReportsSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()
    class Meta:
        model = LabReports
        fields = "__all__"


class DepartmentMappingSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = DepartmentHospitalMapping
        fields = "__all__"
