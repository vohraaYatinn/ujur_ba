from django.db.models import Q

from admin_hospital.models import mainAdminDetails, promoCodes
from doctors.models import doctorDetails, Appointment, PatientDoctorReviews
from hospitals.models import HospitalDetails, HospitalAdmin, LabReports, DepartmentHospitalMapping
from patients.models import Patient


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
        return mainAdminDetails.objects.filter().order_by("-created_at")


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
            filters &= Q(hospital__id=hospital_id)
        return HospitalAdmin.objects.filter(filters).select_related("hospital").order_by("-created_at")

    @staticmethod
    def delete_hospital_admin_by_ujur(data):
        hospital_id = data.get("adminId", None)
        hospital_admin = HospitalAdmin.objects.filter(id=hospital_id)
        if hospital_admin:
            hospital_admin[0].delete()
        else:
            raise Exception("There is something wrong with admin id")

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


    @staticmethod
    def fetch_main_admin_dashboard():
        total_patient_count = Patient.objects.count()
        total_hospital_count = HospitalDetails.objects.count()
        total_doctor_count = doctorDetails.objects.count()
        total_appointment_count = Appointment.objects.count()
        total_admin_count = mainAdminDetails.objects.count()
        total_reviews_count = PatientDoctorReviews.objects.count()
        return {
            "patient":total_patient_count,
            "hospital":total_hospital_count,
            "doctor":total_doctor_count,
            "appointment":total_appointment_count,
            "admin":total_admin_count,
            "reviews":total_reviews_count,
        }


    @staticmethod
    def fetch_main_hospital_dashboard(request):
        hospital_id = request.user.hospital
        appoint_obj = Appointment.objects.filter(doctor__hospital_id=hospital_id)
        total_patient_count = appoint_obj.values('patient').distinct().count()
        total_department_count = DepartmentHospitalMapping.objects.filter(hospital_id=hospital_id).count()
        total_doctor_count = doctorDetails.objects.filter(hospital_id=hospital_id).count()
        total_appointment_count = appoint_obj.count()
        total_admin_count = HospitalAdmin.objects.filter(hospital_id=hospital_id).count()
        total_reviews_count = PatientDoctorReviews.objects.filter(doctor__hospital_id=hospital_id).count()
        return {
            "patient":total_patient_count,
            "department":total_department_count,
            "doctor":total_doctor_count,
            "appointment":total_appointment_count,
            "admin":total_admin_count,
            "reviews":total_reviews_count,
        }


    @staticmethod
    def delete_patient_admin_by_ujur(data):
        hospital_id = data.get("adminId", None)
        hospital_admin = Patient.objects.filter(id=hospital_id)
        if hospital_admin:
            hospital_admin[0].delete()
        else:
            raise Exception("There is something wrong with patient id")


    @staticmethod
    def cancel_appointment_by_ujur(data):
        appointment = data.get("appointmentId", None)
        req_appointment = Appointment.objects.filter(id=appointment)
        if req_appointment:
            req_appointment[0].status = "canceled"
            req_appointment[0].save()
        else:
            raise Exception("There is something wrong with patient id")


    @staticmethod
    def get_promo_code(request):
        return promoCodes.objects.filter().order_by("-created_at")

    @staticmethod
    def add_promo_code(request, data):
        promocode = data.get("promocode", None)
        description = data.get("description", None)
        percentage = data.get("percentage", None)
        if promocode and description and percentage:
            check_if_promo = promoCodes.objects.filter(promocode=promocode).exists()
            if check_if_promo:
                raise Exception("Same Promo code has already been added")
            return promoCodes.objects.create(promocode=promocode, description=description, percentage=percentage)
        else:
            raise Exception("Something is missing in the form")

    @staticmethod
    def delete_promo_code(request, data):
        promocodeId = data.get("promocodeId", None)
        if promocodeId:
            check_if_promo = promoCodes.objects.filter(id=promocodeId)
            if check_if_promo:
                check_if_promo[0].delete()
            else:
                raise Exception("Same Promo code has already been added")
        else:
            raise Exception("Something is missing in the form")

    @staticmethod
    def delete_promo_code(request, data):
        promocodeId = data.get("promocodeId", None)
        if promocodeId:
            check_if_promo = promoCodes.objects.filter(id=promocodeId)
            if check_if_promo:
                check_if_promo[0].delete()
            else:
                raise Exception("Same Promo code has already been added")
        else:
            raise Exception("Something is missing in the form")