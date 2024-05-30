from rest_framework import serializers

from doctors.models import doctorDetails
from hospitals.models import HospitalDetails, Department, LabReports, DepartmentHospitalMapping, HospitalAdmin
from patients.models import Patient




class HospitalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalAdmin
        fields = "__all__"


class DoctorModelForHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctorDetails
        fields = "__all__"



class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDetails
        fields = "__all__"

class HospitalWithAccountSerializer(serializers.ModelSerializer):
    hospital_details_account = HospitalAccountSerializer(many=True)
    class Meta:
        model = HospitalDetails
        fields = "__all__"

class HospitalWithReviewSerializer(serializers.ModelSerializer):
    average_review_stars = serializers.FloatField()
    total_review_stars = serializers.IntegerField()
    class Meta:
        model = HospitalDetails
        fields = "__all__"


class HospitalSerializerWithDoctors(serializers.ModelSerializer):
    hospital_doctors = DoctorModelForHospitalSerializer(many=True)
    class Meta:
        model = HospitalDetails
        fields = "__all__"

class HospitalSerializerWithDoctorsAndAccount(serializers.ModelSerializer):
    hospital_details_account = HospitalAccountSerializer(many=True)
    hospital_doctors = DoctorModelForHospitalSerializer(many=True)
    class Meta:
        model = HospitalDetails
        fields = "__all__"

class HospitalSerializerWithRatingDoctors(serializers.ModelSerializer):
    hospital_doctors = DoctorModelForHospitalSerializer(many=True)
    average_review_stars = serializers.FloatField()
    total_review_stars = serializers.IntegerField()
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


class DoctorModelForHospitalWithDeparmentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = doctorDetails
        fields = "__all__"
