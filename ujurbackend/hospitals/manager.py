import razorpay
from django.db.models import Q, Count, Avg, Prefetch
from django.db.models.functions import Round
import jwt

from doctors.models import doctorDetails, Appointment, PatientDoctorReviews, HospitalPatientReviews
from hospitals.models import HospitalDetails, LabReports, HospitalAdmin, DepartmentHospitalMapping, Department, \
    MedicinesName, ReferToDoctors
from patients.models import Patient
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db import transaction


from ujurbackend import settings

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


class HospitalManager:
    @staticmethod
    def fetch_dashboard_hospital(data):
        return HospitalDetails.objects.filter().annotate(
    average_review_stars=Avg('hospital_reviews__reviews_star'),
            total_review_stars=Count('hospital_reviews__id')
)[:int(data.get("pageNumber"))]

    @staticmethod
    def fetch_doctors_hospital(dataReq, data):
        filters = Q(hospital_id=data.get("hospitalId"))
        doctor_name = dataReq.get('doctorName', False)
        department = dataReq.get('department', False)
        if doctor_name:
            filters &= Q(full_name__icontains = doctor_name)
        if department:
            filters &= Q(department=department)
        return doctorDetails.objects.filter(filters).select_related("department")


    @staticmethod
    def fetch_all_doctors_hospital(hospital_id):
        hospital = HospitalDetails.objects.filter(id=hospital_id).prefetch_related("hospital_doctors").prefetch_related("hospital_details_account")[0]
        reviews=[]
        if hospital:
            doctor_ids = [doctor.id for doctor in hospital.hospital_doctors.all()]
            reviews = PatientDoctorReviews.objects.filter(doctor_id__in=doctor_ids).select_related("doctor").select_related("patient")[:6]
        return hospital, reviews

    @staticmethod
    def fetch_each_doctors_hospital(hospital_id):
        return doctorDetails.objects.filter(hospital_id=hospital_id).select_related("department")



    @staticmethod
    def fetch_completed_doctor_graph(data):
        hospital = data.get("hospitalSearch", False)
        patient = data.get("patientName", False)
        filters = Q()
        if hospital:
            filters &= Q(hospital_id=hospital)
        if patient:
            filters &= Q(patient__full_name__icontains=patient)
        reviews = HospitalPatientReviews.objects.filter(filters).select_related("hospital").select_related("patient")
        return reviews

    @staticmethod
    def fetch_all_hospital_reviews(data):
        hospital = data.get("hospitalSearch", False)
        patient = data.get("patientName", False)
        filters = Q()
        if hospital:
            filters &= Q(hospital_id=hospital)
        if patient:
            filters &= Q(patient__full_name__icontains=patient)
        reviews = HospitalPatientReviews.objects.filter(filters).select_related("hospital").select_related("patient")
        return reviews

    @staticmethod
    def edit_admin_hospital(hospital_id, data):
        hospital_obj = HospitalDetails.objects.get(id=hospital_id)
        hospital_name = data.get("hospital_name", None)
        email = data.get("email", None)
        phone = data.get("phoneNumber", None)
        website = data.get("website", None)
        address = data.get("address", None)
        description = data.get("description", None)
        logo = data.get("logo", None)
        profile = data.get("profile", None)
        google_maps = data.get("googleMap", None)
        years_of_establishment = data.get("years_of_establishment", None)

        if hospital_name:
            hospital_obj.name=hospital_name
        if email:
            hospital_obj.email=email
        if phone:
            hospital_obj.contact_number=phone
        if website:
            hospital_obj.website=website
        if logo:
            hospital_obj.logo=logo
        if logo:
            hospital_obj.hospital_image=profile
        if description:
            hospital_obj.description=description
        if address:
            hospital_obj.address=address
        hospital_obj.google_link=google_maps
        if years_of_establishment:
            hospital_obj.years_of_establishment=years_of_establishment
        hospital_obj.save()


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
        return HospitalDetails.objects.filter(filters).order_by("created_at").prefetch_related("hospital_details_account")

    @staticmethod
    def fetch_lab_reports(request):
        return LabReports.objects.filter(Patients_id=request.user.id).select_related("hospital")

    @staticmethod
    def hospital_admin_login_check(data):
            email = data.get("email")
            password = data.get("password")
            hospital_admin = HospitalAdmin.objects.filter(ujur_id=email, password=password)
            if hospital_admin.exists():
                return hospital_admin[0]
            return False

    @staticmethod
    def fetch_hospital_departments(request, data):
        department = data.get('department', False)
        hospitalId = data.get('hospitalId', False)
        if not hospitalId:
            token = request.headers.get("jwtToken")
            if not token:
                raise Exception("You are not allowed")
            decoded_token = jwt.decode(token, "secretKeyRight34", algorithms=['HS256'])
            if decoded_token and decoded_token.get("hospital", False):
                hospitalId = decoded_token.get("hospital")
        filters = Q(hospital_id=hospitalId)
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
    @transaction.atomic
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
    @transaction.atomic
    def add_admin_hospital(request, data):
        hospital_name = data.get("hospitalName", None)
        email = data.get("email", None)
        phone = data.get("phoneNumber", None)
        website = data.get("website", None)
        address = data.get("address", None)
        description = data.get("description", None)
        logo = data.get("logo", None)
        profile = data.get("profile", None)
        google_link = data.get("googleMap", None)
        years_of_establishment = data.get("yearsofestablishment", None)
        latest_ujur_id=False
        if hospital_name and email and phone and logo and profile and years_of_establishment:
            try:
                latest_hospital_admin = HospitalAdmin.objects.latest('id')
                latest_ujur_id = latest_hospital_admin.ujur_id
            except HospitalAdmin.DoesNotExist:
                new_id_to_add = "CMG101"
            if latest_ujur_id:
                numeric_part = int(latest_ujur_id[3:])
                new_numeric_part = numeric_part + 1
                new_id_to_add = f'CMG{new_numeric_part}'
            else:
                new_id_to_add = "CMG101"
            hospital_proj = HospitalDetails.objects.create(name=hospital_name, email=email, contact_number=phone, logo=logo,  address=address, hospital_image=profile, years_of_establishment=years_of_establishment)
            new_hospital_admin = HospitalAdmin.objects.create(ujur_id= new_id_to_add, name=hospital_name, username=email, password="demo@123", hospital=hospital_proj)
            if website:
                hospital_proj.website = website
            if description:
                hospital_proj.description = description
            if google_link:
                hospital_proj.google_link = google_link
            hospital_proj.save()
        else:
            raise Exception("Something is missing or duplicate entry, Please check email and phone number should be unique and not in use, Hospital image should be added")
    @staticmethod
    def fetch_hospital_admin_data(request, data):
        hospital_id = request.user.hospital
        filters = Q(hospital_id=hospital_id)
        return HospitalAdmin.objects.filter(filters).select_related("hospital").order_by("-created_at")

    @staticmethod
    @transaction.atomic
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
    @transaction.atomic
    def add_medicines_hospital(request, data):
        medicines_name = data.get("name", None)
        medicines_description = data.get("description", None)
        if medicines_name:
            return MedicinesName.objects.create(
                hospital_id=request.user.hospital,
                name = medicines_name,
                description = medicines_description
            )
        else:
            raise Exception("No Data is provided")
    @staticmethod
    def fetch_refer_to_hospital(request, data):
        return ReferToDoctors.objects.filter(hospital=request.user.hospital)

    @staticmethod
    @transaction.atomic
    def add_refer_to_hospital(request, data):
        doctor_name = data.get("doctorName")
        hospital_name = data.get("hospitalName")
        if doctor_name and hospital_name:
            return ReferToDoctors.objects.create(
                hospital_id=request.user.hospital,
                name = doctor_name + " - " + hospital_name
            )

    @staticmethod
    def fetch_doctors_hospital_patient(dataReq, data):
        filters = Q(id=data.get("hospitalId"))
        prefetch_check = Prefetch("hospital_doctors", doctorDetails.objects.filter().annotate(avg_reviews=Round(Avg("doctor_reviews__reviews_star"),1),total_reviews=Count("doctor_reviews__id")), to_attr="hospital_doctors_check")
        return HospitalDetails.objects.filter(filters).prefetch_related(prefetch_check).annotate(
    average_review_stars=Avg('hospital_reviews__reviews_star'),
            total_review_stars=Count('hospital_reviews__id')
)[0]


    @staticmethod
    def cancel_appointment_hospital(request, data):
        appointmentId = data.get("appointmentId")
        hospital = request.user.hospital
        if appointmentId:
            req_appointment = Appointment.objects.get(id=appointmentId, doctor__hospital_id=hospital)
            if not req_appointment:
                raise Exception("No appointment")
            req_appointment.status = "canceled"
            req_appointment.save()

        else:
            raise Exception("appointment id is not valid")

    @staticmethod
    def delete_hospital_admin(request, data):
        adminId = data.get("adminId")
        if adminId:
            req_admin = HospitalAdmin.objects.get(id=adminId, hospital_id=request.user.hospital)
            req_admin.save()

        else:
            raise Exception("Something Went Wrong")

    @staticmethod
    def appointment_action_hospital(request, data):
        appointment_id = data.get("selectedAppointment")
        action = data.get("action")
        if appointment_id and action:
            req_admin = Appointment.objects.get(id=appointment_id)
            if action == "cancel":
                req_admin.status = "cancel"
                req_admin.cancel_reason = "Appointment cancelled by hospital"
                if req_admin.razorpay_payment_id:
                    try:
                        if req_admin.razorpay_payment_id:
                            razorpay_client.payment.refund(req_admin.razorpay_payment_id)
                    except:
                        pass
            if action == "Paid":
                req_admin.payment_status = "Paid"
            if action == "Not Paid":
                req_admin.payment_status = "Not Paid"
            req_admin.save()

        else:
            raise Exception("Something Went Wrong")

    @staticmethod
    def upload_lab_report(request, data):
        appointment = data.get("appointmentId", False)
        lab_report = data.get("labReport", False)
        if appointment:
            req_admin = Appointment.objects.get(id=appointment)
            req_admin.lab_report = lab_report
            req_admin.save()
        else:
            raise Exception("Something Went Wrong")

    @staticmethod
    def edit_hospital_admin_password(request, data):
        admin_id = data.get("adminId")
        password = data.get("password")
        if admin_id and password:
            req_admin = HospitalAdmin.objects.get(id=admin_id)
            req_admin.password = password
            req_admin.save()

        else:
            raise Exception("Something Went Wrong")


    @staticmethod
    def edit_patient_admin_password(request, data):
        patient_id = data.get("patientId")
        password = data.get("password")
        if patient_id and password:
            req_password = Patient.objects.get(id=patient_id)
            req_password.user.password = password
            req_password.user.save()
        else:
            raise Exception("Something Went Wrong")


    @staticmethod
    def analytics_graphs_hospital(request, data):
        today = now().date()
        period = data.get("time", "week")
        if period == 'week':
            start_date = today - timedelta(days=today.weekday())
        elif period == 'month':
            start_date = today.replace(day=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
        else:
            start_date = today.replace(day=1)
        department_patient_count = Appointment.objects.filter(
        date_appointment__gte=start_date, doctor__hospital=request.user.hospital
    ).values(
            'doctor__department__name'
        ).annotate(
            patient_count=Count('patient')
        ).order_by('-patient_count')
        department_patient_count_dict = {}
        for entry in department_patient_count:
            department_patient_count_dict[entry['doctor__department__name']] = entry['patient_count']
        return department_patient_count_dict


    @staticmethod
    def gender_analytics_graphs_hospital(request, data):
        today = now().date()
        period = data.get("time", "week")
        if period == 'week':
            start_date = today - timedelta(days=today.weekday())
        elif period == 'month':
            start_date = today.replace(day=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
        else:
            start_date = today.replace(day=1)
        department_patient_count = Appointment.objects.filter(
        date_appointment__gte=start_date, doctor__hospital=request.user.hospital
    ).values(
            'patient__gender'
        ).annotate(
            patient_count=Count('patient')
        ).order_by('-patient_count')
        department_patient_count_dict = {}
        for entry in department_patient_count:
            department_patient_count_dict[entry['patient__gender']] = entry['patient_count']
        return department_patient_count_dict

    @staticmethod
    def age_analytics_graphs_hospital(request, data):
        today = now().date()
        period = data.get("time", "week")
        if period == 'week':
            start_date = today - timedelta(days=today.weekday())
        elif period == 'month':
            start_date = today.replace(day=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
        else:
            start_date = today.replace(day=1)
        department_patient_count = Appointment.objects.filter(
        date_appointment__gte=start_date, doctor__hospital=request.user.hospital
    ).values(
            'doctor__department__name'
        ).annotate(
            patient_count=Count('patient')
        ).order_by('-patient_count')
        department_patient_count_dict = {}
        for entry in department_patient_count:
            department_patient_count_dict[entry['doctor__department__name']] = entry['patient_count']
        return department_patient_count_dict
