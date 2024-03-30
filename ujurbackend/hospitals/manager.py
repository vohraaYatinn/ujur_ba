from django.db.models import Q

from doctors.models import doctorDetails
from hospitals.models import HospitalDetails, LabReports, HospitalAdmin, DepartmentHospitalMapping, Department


class HospitalManager:
    @staticmethod
    def fetch_dashboard_hospital(data):
        return HospitalDetails.objects.filter()[:int(data.get("pageNumber"))]

    @staticmethod
    def fetch_doctors_hospital(data):
        return HospitalDetails.objects.filter(id=data.get("hospitalId")).prefetch_related("hospital_doctors")[0]

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
        return DepartmentHospitalMapping.objects.filter(hospital_id=request.user.hospital).select_related("department")

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