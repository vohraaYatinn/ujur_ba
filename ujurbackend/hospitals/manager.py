from django.db.models import Q

from doctors.models import doctorDetails
from hospitals.models import HospitalDetails, LabReports, HospitalAdmin, DepartmentHospitalMapping, Department, \
    MedicinesName, ReferToDoctors


class HospitalManager:
    @staticmethod
    def fetch_dashboard_hospital(data):
        return HospitalDetails.objects.filter()[:int(data.get("pageNumber"))]

    @staticmethod
    def fetch_doctors_hospital(dataReq, data):
        filters = Q(hospital_id=data.get("hospitalId"))
        doctor_name = dataReq.get('doctorName', False)
        department = dataReq.get('department', False)
        if doctor_name:
            filters &= Q(full_name__icontains = doctor_name)
        if department:
            filters &= Q(department=department)
        return doctorDetails.objects.filter(filters)

    @staticmethod
    def fetch_all_doctors_hospital(hospital_id):
        return HospitalDetails.objects.filter(id=hospital_id).prefetch_related("hospital_doctors")[0]

    @staticmethod
    def fetch_all_doctors_admin(data):
        filters = Q()
        doctor_name = data.get('doctorName', False)
        department = data.get('department', False)
        hospitals = data.get('hospitalSearch', False)
        if doctor_name:
            filters &= Q(full_name__icontains = doctor_name)
        if department:
            filters &= Q(department=department)
        if hospitals:
            filters &= Q(hospital=hospitals)
        return doctorDetails.objects.filter(filters).prefetch_related("department", "hospital")

    @staticmethod
    def fetch_all_admin_hospital(data):
        hospitals = data.get('hospitalSearch', False)
        filters = Q()
        if hospitals:
            filters &= Q(id=hospitals)
        return HospitalDetails.objects.filter(filters)

    @staticmethod
    def fetch_lab_reports(request):
        return LabReports.objects.filter(Patients_id=request.user.id).select_related("hospital")

    @staticmethod
    def hospital_admin_login_check(data):
            email = data.get("email")
            password = data.get("password")
            hospital_admin = HospitalAdmin.objects.filter(username=email, password=password)
            if hospital_admin.exists():
                return hospital_admin[0]
            return False

    @staticmethod
    def fetch_hospital_departments(request, data):
        department = data.get('department', False)
        filters = Q(hospital_id=request.user.hospital)
        if department:
            filters &= Q(department_id=department)
        return DepartmentHospitalMapping.objects.filter(filters).select_related("department")

    @staticmethod
    def get_departments(department_id):
        return Department.objects.filter(id__in=department_id)

    @staticmethod
    def fetch_all_admin_departments(data):
        department = data.get("department")
        filters = Q()
        if department:
            filters &= Q(id=department)
        return Department.objects.filter(filters)


    @staticmethod
    def add_department_hospital(request, data):
        department_id = data.get("department_id", False)
        if not department_id:
            department_name = data.get("department_name", False)
            department_desc = data.get("department_desc", False)
            department_id = Department.objects.create(name=department_name, description=department_desc)
        return DepartmentHospitalMapping.objects.create(hospital_id=request.user.hospital, department=department_id).select_related("department")

    @staticmethod
    def handle_delete_hospital(data):
        action = data.get("action", None)
        type = data.get("type", None)
        id = data.get("id", None)
        if type and id and action:
            if action == "delete":
                if type == "doctor":
                    return doctorDetails.objects.get(id=id).delete()
                elif type == "hospital":
                    return HospitalDetails.objects.get(id=id).delete()
            elif action == "active":
                doctor = doctorDetails.objects.get(id=id)
                doctor.is_active = not doctor.is_active
                doctor.save()
                return doctor

        else:
            raise Exception("Something is missing in the form")


    @staticmethod
    def add_admin_hospital(request, data):
        hospital_name = data.get("hospitalName", None)
        email = data.get("email", None)
        phone = data.get("phoneNumber", None)
        website = data.get("website", None)
        address = data.get("address", None)
        description = data.get("description", None)
        logo = data.get("logo", None)
        if hospital_name and email and phone and website and description and logo:
            HospitalDetails.objects.create(name=hospital_name, email=email, contact_number=phone, website=website, logo=logo, description=description, address=address)

    @staticmethod
    def fetch_hospital_admin_data(request, data):
        hospital_id = request.user.hospital
        filters = Q(hospital_id=hospital_id)
        return HospitalAdmin.objects.filter(filters).select_related("hospital")

    @staticmethod
    def add_hospital_admin_data(request, data):
        full_name = data.get("fullName", None)
        email = data.get("email", None)
        password = data.get("password", None)
        hospital = request.user.hospital
        return HospitalAdmin.objects.create(
            name=full_name,
            username=email,
            password=password,
            hospital_id=hospital
        )

    @staticmethod
    def fetch_medicines_hospital(request, data):
        return MedicinesName.objects.filter(hospital=request.user.hospital)

    @staticmethod
    def add_medicines_hospital(request, data):
        medicines_name = data.get("name")
        medicines_description = data.get("description")
        if medicines_name and medicines_description:
            return MedicinesName.objects.create(
                hospital_id=request.user.hospital,
                name = medicines_name,
                description = medicines_description
            )
    @staticmethod
    def fetch_refer_to_hospital(request, data):
        return ReferToDoctors.objects.filter(hospital=request.user.hospital)

    @staticmethod
    def add_refer_to_hospital(request, data):
        doctor_name = data.get("doctorName")
        hospital_name = data.get("hospitalName")
        if doctor_name and hospital_name:
            return ReferToDoctors.objects.create(
                hospital_id=request.user.hospital,
                name = doctor_name + " - " + hospital_name
            )
