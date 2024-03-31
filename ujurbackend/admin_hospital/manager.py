from django.db.models import Q

from admin_hospital.models import mainAdminDetails
from doctors.models import doctorDetails
from hospitals.models import HospitalDetails, HospitalAdmin


class AdminMainManagement:
    @staticmethod
    def login_main_admin(data):
        email = data.get("email")
        password = data.get("password")
        check_admin = mainAdminDetails.objects.filter(email=email, password=password)
        if check_admin.exists():
            return check_admin[0]
        return False

    @staticmethod
    def add_admin_form(data):
        full_name = data.get("fullName", None)
        email = data.get("email", None)
        password = data.get("password", None)
        if full_name and email and password:
            return mainAdminDetails.objects.create(full_name=full_name, email=email, password=password)
        else:
            raise Exception("Something is missing in the form")


    @staticmethod
    def fetch_admin_data(data):
        return mainAdminDetails.objects.filter()


    @staticmethod
    def handle_delete_admin(data):
        type = data.get("type", None)
        id = data.get("id", None)
        if type and id:
            if type == "doctor":
                return doctorDetails.objects.get(id=id).delete()
            elif type == "hospital":
                return HospitalDetails.objects.get(id=id).delete()
        else:
            raise Exception("Something is missing in the form")

    @staticmethod
    def fetch_hospital_admin_data(data):
        hospital_id = data.get("hospitalSearch", None)
        filters = Q()
        if hospital_id:
            filters &= Q(id=hospital_id)
        return HospitalAdmin.objects.filter(filters).select_related("hospital")

    @staticmethod
    def add_hospital_admin_data(data):
        full_name = data.get("fullName", None)
        email = data.get("email", None)
        password = data.get("password", None)
        hospital = data.get("HospitalsId", None)
        return HospitalAdmin.objects.create(
            name=full_name,
            username=email,
            password=password,
            hospital_id=hospital
        )

