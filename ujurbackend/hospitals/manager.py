from hospitals.models import HospitalDetails, LabReports, HospitalAdmin, DepartmentHospitalMapping, Department


class HospitalManager:
    @staticmethod
    def fetch_dashboard_hospital(data):
        return HospitalDetails.objects.filter()[:int(data.get("pageNumber"))]

    @staticmethod
    def fetch_doctors_hospital(data):
        return HospitalDetails.objects.filter(id=data.get("hospitalId")).prefetch_related("hospital_doctors")[0]

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
    def add_department_hospital(request, data):
        department_id = data.get("department_id", False)
        if not department_id:
            department_name = data.get("department_name", False)
            department_desc = data.get("department_desc", False)
            department_id = Department.objects.create(name=department_name, description=department_desc)
        return DepartmentHospitalMapping.objects.create(hospital_id=request.user.hospital, department=department_id).select_related("department")
