from sqlite3 import IntegrityError

from doctors.models import doctorDetails, doctorSlots, FavDoctors, Appointment, PatientDoctorReviews, DoctorLeave, \
    ResetPasswordRequest, HospitalPatientReviews, Revenue, getChiefQuery, labTests
from django.db.models import Avg, Count, Prefetch
from django.db.models.functions import Round
from django.db import transaction

from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.db.models import F
from django.utils.timezone import now, timedelta
import razorpay
import os


from hospitals.models import HospitalDetails, Department, DepartmentHospitalMapping, MedicinesName, HospitalAdmin
from patients.models import Patient
from ujurbackend import settings
from users.models import UsersDetails

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


class DoctorsManagement:
    @staticmethod
    def fetch_dashboard_doctor(data):
        return doctorDetails.objects.filter().annotate(
                avg_reviews=Round(Avg("doctor_reviews__reviews_star"),1),
                total_reviews=Count("doctor_reviews__id")
            ).prefetch_related("doctor_slots")[:int(data.get("pageNumber"))]

    @staticmethod
    def fetch_single_doctor(request, data):
        doctor_id = data.get("doctorId")
        return (doctorDetails.objects.filter(id=doctor_id).annotate(
                avg_reviews=Round(Avg("doctor_reviews__reviews_star"),1),
                total_reviews=Count("doctor_reviews__id")
            ).select_related("hospital").select_related("user").select_related("department")[0],
                FavDoctors.objects.filter(patient_id=request.user.id, doctor_id=doctor_id).exists())

    @staticmethod
    def fetch_doctor_slots(data):
        doctor_id = data.get("doctorId")
        start_date = datetime.today()
        dates_and_days = []
        for i in range(6):
            date = start_date + timedelta(days=i)
            dates_and_days.append((date.strftime("%Y-%m-%d"), date.strftime("%A")))
        return doctorSlots.objects.filter(doctor_id=doctor_id).select_related("doctor")[0], dates_and_days

    @staticmethod
    def fav_doctor_select(request, data):
        patient_id = request.user.id
        doctor_id = data.get("doctorId")
        action = data.get("action")

        if patient_id and doctor_id:
            if action == "add":
                FavDoctors.objects.create(
                    patient_id=patient_id,
                    doctor_id=doctor_id
                )
            else:
                fav_doc = FavDoctors.objects.filter(
                    patient_id=patient_id,
                    doctor_id=doctor_id
                )
                fav_doc.delete()
        else:
            raise Exception("There is Something missing in the form, Please Try again")

    @staticmethod
    def fav_doctor_fetch(request, data):
        patient_id = request.user.id
        if patient_id:
            fav_doc = FavDoctors.objects.filter(
                patient_id=patient_id
            ).select_related("doctor")

            return fav_doc
        else:
            raise Exception("There is Something missing in the form, Please Try again")


    @staticmethod
    def book_appointment(data):
        patient_id = data.get("patient_id")
        doctor_id = data.get("doctor_id")
        slot = data.get("slot")
        date_appointment = data.get("date_appointment")
        if patient_id and doctor_id and slot and date_appointment:
            Appointment.objects.create(
                patient_id = patient_id,
                doctor_id = doctor_id,
                slot = slot,
                date_appointment = date_appointment
            )
        else:
            raise Exception("There is Something missing in the form, Please Try again")


    @staticmethod
    def fetch_appointments(data):
        patient_id = data.get("patient_id")
        type =  data.get('type', False)
        if patient_id:
            appointments = Appointment.objects.filter(
                patient_id = patient_id
            ).select_related("doctor")
            return appointments
        else:
            raise Exception("It Looks like you have missed something, Please try again")

    @staticmethod
    def fetch_all_appointments(data):
        filters = Q()
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        date = data.get('date', False)
        slots = data.get('slots', False)
        status = data.get('status', False)
        department = data.get('department', False)
        hospitals = data.get('hospitalSearch', False)
        paymentStatus = data.get('paymentStatus', False)
        paymentMode = data.get('paymentMode', False)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if date:
            filters &= Q(date_appointment__date=date)
        if slots:
            filters &= Q(slot=slots)
        if status:
            filters &= Q(status=status)
        if department:
            filters &= Q(doctor__department=department)
        if hospitals:
            filters &= Q(doctor__hospital=hospitals)
        if paymentStatus:
            filters &= Q(payment_status=paymentStatus)
        if paymentMode:
            filters &= Q(payment_mode=paymentMode)
        appointments = Appointment.objects.filter(filters
        ).select_related("doctor", "patient", "patient__user","doctor__hospital").prefetch_related("revenues").exclude(status="created").order_by("-created_at")
        return appointments

    @staticmethod
    def fetch_all_revenue(data):
        filters = Q()
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        date = data.get('date', False)
        slots = data.get('slots', False)
        status = data.get('status', False)
        department = data.get('department', False)
        hospitals = data.get('hospitalSearch', False)
        paymentStatus = data.get('paymentStatus', False)
        paymentMode = data.get('paymentMode', False)
        startDate = data.get('startDate', False)
        endDate = data.get('endDate', False)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if slots:
            filters &= Q(slot=slots)
        if status:
            filters &= Q(status=status)
        if department:
            filters &= Q(doctor__department=department)
        if hospitals:
            filters &= Q(doctor__hospital=hospitals)
        if paymentStatus:
            filters &= Q(payment_status=paymentStatus)
        if paymentMode:
            filters &= Q(payment_mode=paymentMode)
        if startDate:
            filters &= Q(date_appointment__date__gte=startDate)
        if endDate:
            filters &= Q(date_appointment__date__lte=endDate)
        appointments = Appointment.objects.filter(filters
        ).select_related("doctor", "patient", "patient__user").prefetch_related("revenues").exclude(status="created").order_by("-created_at")
        return appointments

    @staticmethod
    def fetch_all_revenue_hospital(request, data):
        filters = Q()
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        date = data.get('date', False)
        slots = data.get('slots', False)
        status = data.get('status', False)
        department = data.get('department', False)
        hospitals = request.user.hospital
        paymentStatus = data.get('paymentStatus', False)
        paymentMode = data.get('paymentMode', False)
        startDate = data.get('startDate', False)
        endDate = data.get('endDate', False)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if slots:
            filters &= Q(slot=slots)
        if status:
            filters &= Q(status=status)
        if department:
            filters &= Q(doctor__department=department)
        if hospitals:
            filters &= Q(doctor__hospital=hospitals)
        if paymentStatus:
            filters &= Q(payment_status=paymentStatus)
        if paymentMode:
            filters &= Q(payment_mode=paymentMode)
        if startDate:
            filters &= Q(date_appointment__date__gte=startDate)
        if endDate:
            filters &= Q(date_appointment__date__lte=endDate)
        appointments = Appointment.objects.filter(filters
        ).select_related("doctor", "patient", "patient__user").prefetch_related("revenues").exclude(status="created").order_by("-created_at")
        return appointments


    @staticmethod
    def patient_doctor_reviews(request, data):
        patient_id = request.user.id
        if patient_id:
            reviews = PatientDoctorReviews.objects.filter(
                patient_id = patient_id
            ).select_related("doctor")
            return reviews
        else:
            raise Exception("It Looks like you have missed something, Please try again")


    @staticmethod
    def hospital_reviews(request, data):
        reviews = PatientDoctorReviews.objects.filter(
            doctor__hospital_id=request.user.hospital
        ).select_related("doctor").select_related("patient")
        return reviews

    @staticmethod
    def self_hospital_reviews(request, data):
        star_review = data.get("starSearch", False)
        filters = Q(hospital_id=request.user.hospital)

        if star_review:
            filters &= Q(reviews_star=star_review)
        reviews = HospitalPatientReviews.objects.filter(filters

        ).select_related("hospital").select_related("patient")
        return reviews

    @staticmethod
    def self_graph_gender_and_age(request, data):
        patient_name = data.get("patientName", False)
        filters = Q(hospital_id=request.user.hospital)
        if patient_name:
            filters &= Q(patient__full_name__icontains=patient_name)
        reviews = HospitalPatientReviews.objects.filter(filters

        ).select_related("hospital").select_related("patient")
        return reviews

    @staticmethod
    def all_patients_admin(request, data):
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)

        filters = Q()
        if patient_name:
            filters &= Q(full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(full_name__icontains = doctor_name)
        unique_patients = Patient.objects.filter(filters).select_related("user").order_by("-created_at")
        return unique_patients

    @staticmethod
    def all_patients_hospital(request, data):
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        department = data.get('department', False)

        filters = Q(doctor__hospital_id=request.user.hospital)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if department:
            filters &= Q(doctor__department=department)
        patient_ids = Appointment.objects.filter(filters).values('patient').distinct()
        unique_patients = Patient.objects.filter(id__in=patient_ids).order_by("-created_at").select_related("user")
        return unique_patients


    @staticmethod
    @transaction.atomic
    def add_patients_hospital(request, data):
        try:
            phone_number = data.get("phoneNumber")
            full_name = data.get("fullName")
            gender = data.get("gender")
            email = data.get("email")
            date_of_birth = data.get("dob")
            blood_group = data.get("bloodGroup")
            weight = data.get("weight")
            district = data.get("district")
            user = UsersDetails.objects.create(phone=phone_number, email=email)
            if email:
                user.email = email
                user.save()
            new_patient = Patient.objects.create(
                user=user,
                full_name=full_name,
                gender=gender,
                date_of_birth=date_of_birth,

                address=district
            )
            if blood_group:
                new_patient.blood_group = blood_group
            if weight:
                new_patient.weight = weight
            new_patient.save()
            return new_patient
        except IntegrityError as e:
            raise Exception (f"IntegrityError: {e}")

    @staticmethod
    def patient_doctor_reviews_create(request, data):
        patient_id = request.user.id
        doctor_id = data.get("doctor_id")
        reviews = data.get("reviews")
        if patient_id and doctor_id and reviews:
            appointments = PatientDoctorReviews.objects.create(
                patient_id = patient_id,
                doctor_id=doctor_id,
                reviews_star=reviews
            )
        else:
            raise Exception("It Looks like you have missed something, Please try again")

    @staticmethod
    @transaction.atomic
    def patient_appointment_book(request, data):
        patient_id = request.user.id
        doctor_id = data.get("doctorId")
        date = data.get("date")
        slot = data.get("slot")
        comment = data.get("comment")
        document = data.get("document")

        if patient_id and doctor_id and date and slot:
            check_if_already_exist = Appointment.objects.filter(
                patient_id=patient_id,
                doctor_id=doctor_id,
                slot=slot,
                date_appointment=date,
            ).exclude(status="created")
            if check_if_already_exist:
                raise Exception("The appointment is already booked in this slot.")
            latest_appointment_slot = Appointment.objects.filter(
                    doctor_id=doctor_id,
                    date_appointment__date=date,
                    slot=slot
                    ).exclude(status="created")
            latest_appointment = latest_appointment_slot.order_by('-appointment_slot').first()
            if latest_appointment:
                latest_slot = latest_appointment.appointment_slot
            else:
                latest_slot = 0
            doctor_slots = doctorSlots.objects.get(doctor__id=doctor_id)
            if slot == "morning":
                slot_number = doctor_slots.morning_slots
            elif slot == "afternoon":
                slot_number = doctor_slots.afternoon_slots
            elif slot == "evening":
                slot_number = doctor_slots.evening_slots
            if int(latest_slot)+1 <= int(slot_number):
                appointment = Appointment.objects.create(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    slot=slot,
                    date_appointment=date,
                    patients_query=comment
                )
                if document:
                    appointment.patient_documents = document
                appointment.save()

                return appointment.id
            else:
                raise Exception("It Looks like slots for this has already been fulled")
        else:
            raise Exception("It Looks like you have missed something, Please try again")

    @staticmethod
    def get_booking_price(data):
        booking_id = data.get("bookingId")
        if booking_id:
            try:
                appointment = Appointment.objects.get(
                    id=booking_id
                )
            except:
                raise Exception("There is something wrong with your booking, Contact Customer Support for this Issue")
            if appointment:
                price = False
                doctor_slots = doctorSlots.objects.get(doctor=appointment.doctor)
                if appointment.slot == "morning":
                    price = doctor_slots.morning_slots_price
                elif appointment.slot == "afternoon":
                    price = doctor_slots.afternoon_slots_price
                elif appointment.slot == "evening":
                    price = doctor_slots.evening_slots_price
                return price
            else:
                raise Exception
        else:
            raise Exception("It Looks like you have missed something, Please try again")

    @staticmethod
    @transaction.atomic
    def patient_booking_confirmation(data):
        booking_id = data.get("bookingId")
        paymentMode = data.get("paymentMode")
        bookingAmount = data.get("bookingAmount")
        payment_status = "Not Paid"

        if paymentMode == "Online":
            payment_status = "Paid"
        if booking_id:
            appointment = Appointment.objects.filter(
                id=booking_id
            ).select_related("doctor")[0]
            latest_appointment_slot = Appointment.objects.filter(
                    date_appointment=appointment.date_appointment,
                    slot=appointment.slot,
                    doctor=appointment.doctor,
                    ).exclude(status="created")
            latest_appointment = latest_appointment_slot.order_by('-appointment_slot').first()
            if latest_appointment:
                latest_slot = latest_appointment.appointment_slot
            else:
                latest_slot = 0
            appointment.status = "pending"
            appointment.payment_mode = paymentMode
            appointment.payment_status = payment_status
            appointment.appointment_slot = int(latest_slot) + 1
            appointment.save()
            Revenue.objects.create(appointment=appointment,booking_amount=10, doctor_fees=float(bookingAmount-10))
            return True, appointment
        else:
            raise Exception("It Looks like you have missed something, Please try again")

    @staticmethod
    def fetch_patient_latest_appointment(request, data):
        patient_id = request.user.id
        if patient_id:
            latest_appointment = Appointment.objects.filter(
                patient_id=patient_id,
                status="pending"
            ).select_related("doctor").exclude(status="created").order_by("-created_at")
            if latest_appointment:
                return latest_appointment[0]
            else:
                return []
        else:
            raise Exception("It Looks like you have missed something, Please try again")


    @staticmethod
    def fetch_appointment_details(request, data):
        patient_id = request.user.id
        appointment_type = data.get("appointmentType")
        filters = Q()
        filters &= Q(patient_id=patient_id)
        if patient_id and appointment_type:
            if appointment_type == "upcoming":
                filters &= Q(status="pending") | Q(status="queue")
            elif appointment_type == "completed":
                filters &= Q(status="completed")
            else:
                filters &= Q(status="cancel")
            latest_appointment = Appointment.objects.filter(filters
            ).select_related("doctor").order_by("-created_at")
            return latest_appointment
        else:
            raise Exception("It Looks like you have missed something, Please try again")

    @staticmethod
    def fetch_appointment_details_per_appointment(data):
        appointment_id = data.get("appointmentId")
        if appointment_id:
            latest_appointment = Appointment.objects.filter(
                id=appointment_id
            ).select_related("doctor").select_related("patient", "patient__user").select_related("doctor__hospital").prefetch_related("revenues").order_by("-created_at")
            slot = latest_appointment[0].slot
            date = latest_appointment[0].date_appointment

            if latest_appointment:
                slots = doctorSlots.objects.get(doctor=latest_appointment[0].doctor)
                return latest_appointment[0], slots, Appointment.objects.filter(date_appointment=date, slot=slot ,doctor=latest_appointment[0].doctor
                           ).exclude(status="created").exclude(status="cancel").count()
            else:
                return []
        else:
            raise Exception("It Looks like you have missed something, Please try again")


    @staticmethod
    def login_doctor(request, data):
        email = data.get("email")
        password = data.get("password")
        check_doctor = doctorDetails.objects.filter(ujur_id=email, password=password).select_related("hospital")
        if check_doctor.exists():
            return check_doctor[0]
        return False

    @staticmethod
    def doctor_leave_fetch(request, data):
        filters = Q(doctor__hospital_id=request.user.hospital)
        doctor_name = data.get('doctorName', False)
        department = data.get('department', False)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if department:
            filters &= Q(doctor__department=department)
        doctor_leave = DoctorLeave.objects.filter(filters).select_related("doctor")
        return doctor_leave

    @staticmethod
    def fetch_hospital_appointments(request, data):
        filters = Q(doctor__hospital_id=request.user.hospital)
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        date = data.get('date', False)
        slots = data.get('slots', False)
        status = data.get('status', False)
        department = data.get('department', False)
        paymentStatus = data.get('paymentStatus', False)
        paymentMode = data.get('paymentMode', False)

        if paymentStatus:
            filters &= Q(payment_status=paymentStatus)
        if paymentMode:
            filters &= Q(payment_mode=paymentMode)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if date:
            filters &= Q(date_appointment__date=date)
        if slots:
            filters &= Q(slot=slots)
        if status:
            filters &= Q(status=status)
        if department:
            filters &= Q(doctor__department=department)
        doctor_leave = Appointment.objects.filter(filters).exclude(status="created").select_related("doctor", "doctor__hospital").prefetch_related("revenues").select_related("patient", "patient__user").order_by("-created_at", "appointment_slot")
        return doctor_leave

    @staticmethod
    def doctor_self_appointment_fetch(request, data):
        patient_name = data.get("patientName")
        date = data.get("date")
        selected_date = datetime.strptime(date, "%Y-%m-%d")
        slot = data.get("slot", False)
        status = data.get("status", False)
        filters = Q()
        filters &= Q(doctor_id=request.user.doctor)
        filters &= Q(date_appointment__date=selected_date)
        if slot:
            filters &= Q(slot=slot)
        if status:
            filters &= Q(status=status)
        if patient_name:
            filters &= Q(patient__full_name__icontains=patient_name)
        latest_appointment = Appointment.objects.filter(filters
        ).select_related("patient").select_related("doctor").exclude(status="created").order_by("id")

        return latest_appointment

    @staticmethod
    def hospital_appointments_fetch(request, data):
        date = data.get("date")
        selected_date = datetime.strptime(date, "%Y-%m-%d")
        slot = data.get("slot", False)
        doctor_id = data.get("doctorId", False)
        query = Q()
        if slot:
            query &= Q(slot = slot)
        if doctor_id:
            query &= Q(doctor_id = doctor_id)
        latest_appointment = Appointment.objects.filter(
            doctor__hospital_id=request.user.hospital,
            date_appointment__date=selected_date
        ).filter(query).select_related("patient").exclude(status="created").order_by("-created_at")

        return latest_appointment

    from datetime import datetime, timedelta
    from django.db.models import Count
    from django.utils import timezone
    @staticmethod
    def doctor_dashboard_details(request, data):
        total = []
        pending = []
        canceled = []
        completed = []
        period = data.get("time", "Week")
        time_period_dict = {}
        weekday_aliases = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }
        month_aliases = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }

        if period == 'Week':
            start_of_period = datetime.now() - timedelta(days=datetime.now().weekday())
            end_of_period = start_of_period + timedelta(days=6)
        elif period == 'Month':
            today = datetime.now().date()
            start_of_period = datetime(today.year, today.month, 1)
            end_of_period = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
        elif period == 'Year':
            today = datetime.now().date()
            start_of_period = datetime(today.year, 1, 1)
            end_of_period = datetime(today.year, 12, 31)

        current_date = start_of_period
        index = 0
        while current_date <= end_of_period:
            index += 1
            appointments = Appointment.objects.filter(
                doctor_id=request.user.doctor,
                date_appointment__date=current_date.date(),
            ).values('status').annotate(count=Count('status'))

            total_count = sum(appt['count'] for appt in appointments)
            pending_count = sum(appt['count'] for appt in appointments if appt['status'] == 'pending')
            canceled_count = sum(appt['count'] for appt in appointments if appt['status'] == 'cancel')
            completed_count = sum(appt['count'] for appt in appointments if appt['status'] == 'completed')

            total.append(int(total_count))
            pending.append(int(pending_count))
            canceled.append(int(canceled_count))
            completed.append(int(completed_count))
            if period == 'Week':
                time_period_dict[index] = weekday_aliases[current_date.weekday()]
            if period == 'Month':
                time_period_dict[index] = str(current_date.date())
            if period == 'Year':
                time_period_dict[index] = month_aliases[current_date.month]

            current_date += timedelta(days=1)

        return {
            "total": total,
            "pending": pending,
            "canceled": canceled,
            "completed": completed,
        }, time_period_dict

    @staticmethod
    def doctor_patients_appointments(request, data):
        date = data.get('date', datetime.today().date())
        slot = data.get('slots',False)
        filters = Q(doctor_id=request.user.doctor)

        filters &= Q(date_appointment__date = date)
        if slot:
            filters &= Q(slot = slot)
        pending_appointments_status = Appointment.objects.filter(
            filters & Q(status="queue")
        ).select_related("patient").order_by("-created_at")
        pending_appointments = Appointment.objects.filter(
            filters & Q(status="pending")
        ).select_related("patient").order_by("date_appointment")
        canceled_appointments = Appointment.objects.filter(
            filters & Q(status="cancel")
        ).select_related("patient").order_by("date_appointment")
        completed_appointments = Appointment.objects.filter(
            filters & Q(status="completed")
        ).select_related("patient").order_by("date_appointment")

        return {
            'total_appointments': pending_appointments,
            'pending_appointments': pending_appointments_status,
            'canceled_appointments': canceled_appointments,
            'completed_appointments': completed_appointments,
        }

    @staticmethod
    def patient_searching(request, data):
        search_keyword = data.get('searchInput')
        doctors = doctorDetails.objects.filter(
            Q(full_name__icontains=search_keyword) |
            Q(specialization__icontains=search_keyword) |
            Q(education__icontains=search_keyword) |
            Q(department__name__icontains=search_keyword) |
            Q(hospital__name__icontains=search_keyword)
        ).select_related("hospital")[:4]

        hospitals = HospitalDetails.objects.filter(
            Q(name__icontains=search_keyword) |
            Q(description__icontains=search_keyword) |
            Q(address__icontains=search_keyword)
        )[:4]

        list_to_give = []
        for i in doctors:
            list_to_give.append({
                "id":i.id,
                "name":i.full_name,
                "batch":"doctor",
                "img": str(i.profile_picture),
                "hospital": i.hospital.name

            })
        for i in hospitals:
            list_to_give.append({
                "id": i.id,
                "name":i.name,
                "batch":"hospital",
                "img": str(i.logo)

            })
        return list_to_give

    @staticmethod
    def doctor_fetch_patients(request, data):
        patient_name = data.get("patientName")
        filters = Q(doctor_id = request.user.doctor)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        appointments_with_specific_doctor = Appointment.objects.filter(filters)
        patients_with_appointments = appointments_with_specific_doctor.values_list('patient', flat=True).distinct()
        patients = Patient.objects.filter(id__in=patients_with_appointments).select_related("user")
        return patients

    @staticmethod
    def all_doctor_patients(request, data):
        number_of_page = data.get("pageNumber", 1)
        return doctorDetails.objects.filter().annotate(
                avg_reviews=Round(Avg("doctor_reviews__reviews_star"),1),
                total_reviews=Count("doctor_reviews__id")
            ).prefetch_related("doctor_slots").prefetch_related("department", "hospital")[:int(number_of_page)*20]

    @staticmethod
    def all_hospital_patients(request, data):
        number_of_page = data.get("pageNumber", 1)
        return HospitalDetails.objects.filter()[:int(number_of_page)*20]

    @staticmethod
    def all_available_slots(request, data):
        doctor_id = data.get("doctorId", False)
        date = data.get("date", False)
        if not date:
            raise Exception("date is required")
        available_slots = {
            "morning":0,
            "afternoon":0,
            "evening":0
        }
        doctor_slots = doctorSlots.objects.filter(doctor__id=doctor_id)
        total_morning_slots = doctor_slots[0].morning_slots
        total_afternoon_slots = doctor_slots[0].afternoon_slots
        total_evening_slots = doctor_slots[0].evening_slots
        if total_morning_slots:
            total_morning_appointments = Appointment.objects.filter(date_appointment__date=date, doctor__id=doctor_id, slot="morning").exclude(status="canceled").exclude(status="created").count()
            count = total_morning_slots - total_morning_appointments
            if count < 0:
                count = 0
            available_slots["morning"] = count
        if total_afternoon_slots:
            total_afternoon_appointments = Appointment.objects.filter(date_appointment__date=date, doctor__id=doctor_id, slot="afternoon").exclude(status="canceled").exclude(status="created").count()
            count = total_afternoon_slots - total_afternoon_appointments
            if count < 0:
                count = 0
            available_slots["afternoon"] = count
        if total_evening_slots:
            total_evening_appointments = Appointment.objects.filter(date_appointment__date=date, doctor__id=doctor_id, slot="evening").exclude(status="canceled").exclude(status="created").count()
            count = total_evening_slots - total_evening_appointments
            if count < 0:
                count = 0
            available_slots["evening"] = count
        return available_slots

    @staticmethod
    def doctor_prescription_download(request, data):
        appointment =  Appointment.objects.filter(id=258)
        appointment[0].prescription = data['file']
        appointment[0].save()


    @staticmethod
    def doctor_fetch_reviews(request, data):
        filters = Q(doctor_id=request.user.doctor)
        star_search = data.get("starSearch", False)
        if star_search == "false":
            star_search = False
        date = data.get("date", False)
        if star_search:
            filters &= Q(reviews_star = star_search)
        if date:
            filters &= Q(created_at__date = date)

        reviews_objs = PatientDoctorReviews.objects.filter(
            filters).select_related("patient")
        # Initialize counts for each star rating
        star_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_sum = 0
        for rating_count in reviews_objs:
            star_counts[rating_count.reviews_star] = star_counts[rating_count.reviews_star] + 1
            total_sum = total_sum + rating_count.reviews_star
        if total_sum:
            total_sum = round(total_sum / len(reviews_objs),2)
        else:
            total_sum = 0

        return {
            "star_counts": star_counts,
            "average_rating": total_sum,
            "reviews_objs": reviews_objs
        }

    @staticmethod
    def doctor_fetch_reviews_top_5(request, data):
        reviews_objs = PatientDoctorReviews.objects.filter(
            doctor_id=request.user.doctor).select_related("patient").order_by("-created_at")[:5]
        return reviews_objs


    @staticmethod
    def fetch_my_profile_doctor(request, data):
        doctor_obj = doctorDetails.objects.select_related("user").get(
            id=request.user.doctor)
        return doctor_obj

    @staticmethod
    def fetch_hospital_doctor_profile(request, data):
        doctor_id = data.get('doctor_id')
        doctor_obj = {}
        if doctor_id:
            doctor_obj = doctorDetails.objects.filter(id=doctor_id).annotate(
                avg_reviews=Round(Avg("doctor_reviews__reviews_star"),1),
                total_reviews=Count("doctor_reviews__id")
            ).prefetch_related("doctor_slots").prefetch_related("doctor_reviews").select_related('user').select_related("department").select_related("hospital")
        return doctor_obj[0]

    @staticmethod
    def doctor_change_password(request, data):
        old_password = data.get("oldPassword", False)
        new_password = data.get("newPassword", False)
        if old_password and new_password:
            doctor_obj = doctorDetails.objects.filter(
                id=request.user.doctor, password=old_password)
            if doctor_obj:
                doctor_obj[0].password = new_password
                doctor_obj[0].save()
            else:
                raise Exception("Invalid Old Password")
        else:
            raise Exception("You are missing something")


    @staticmethod
    def doctor_change_profile(request, data):
        email = data.get("email", False)
        phone_number = data.get("phoneNumber", False)
        bio = data.get("bio", False)
        doctor_obj = doctorDetails.objects.filter(
            id=request.user.doctor)
        if doctor_obj:
            if email:
                doctor_obj[0].user.email = email
                doctor_obj[0].email = email
            if phone_number:
                doctor_obj[0].user.phone = phone_number
            if bio:
                doctor_obj[0].bio = bio
            doctor_obj[0].user.save()
            doctor_obj[0].save()

        else:
            raise Exception("You are missing something")
    @staticmethod
    def fetch_patient_profile(request, data):
        patientId = data.get("patientId", False)
        if patientId:
            prefetch_value = Prefetch("patient_appointments", Appointment.objects.order_by("-date_appointment").order_by("-created_at"), to_attr="appointments")
            patient_obj = Patient.objects.filter(
                id=patientId).prefetch_related(prefetch_value).select_related("user")
            return patient_obj
        else:
            raise Exception("You are missing something")


    @staticmethod
    def patient_prescription_upload(request, data):
        htmlContent = data.get("htmlContent", False)
        appointmentDetails = data.get("appointmentDetails", False)
        doctorComment = data.get("doctorComment", False)
        prescription_method = data.get("prescriptionMethod", False)
        if prescription_method == "manual":
            pdf = False

        else:
            pdf = request.FILES['pdf']
        if htmlContent and prescription_method == "digital" and appointmentDetails:
            appointment_obj = Appointment.objects.get(id=appointmentDetails)
            file_name = f"Prescription_{appointment_obj.patient.full_name}_{appointment_obj.id}_{datetime.now().strftime('%d-%m-%Y')}.pdf"
            appointment_obj.pdf_content = htmlContent
            if doctorComment:
                appointment_obj.doctor_instruction = doctorComment
            appointment_obj.status = "completed"
            appointment_obj.prescription = pdf
            appointment_obj.prescription.name = file_name
            appointment_obj.save()
        elif prescription_method == "manual":
            appointment_obj = Appointment.objects.get(id=appointmentDetails)
            appointment_obj.status = "completed"
            appointment_obj.prescription_method = "manual"
            appointment_obj.save()

        else:
            raise Exception("You are missing something")

    @staticmethod
    def doctor_leave_get(request, data):
        leaves = DoctorLeave.objects.filter(doctor=request.user.doctor)
        return leaves

    @staticmethod
    def apply_leave(request, data):
        from_date = data.get("fromDate", None)
        to_date = data.get("toDate", None)
        comment = data.get("comment", None)
        DoctorLeave.objects.create(doctor_id=request.user.doctor, from_date=from_date, to_date=to_date,comment=comment )

    @staticmethod
    def fetch_reset_request(request, data):
        doctor_name = data.get('doctorName', False)
        department = data.get('department', False)
        filters = Q(hospital_id=request.user.hospital)
        if department:
            filters &= Q(doctor__department_id=department)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        return ResetPasswordRequest.objects.filter(doctor__hospital_id=request.user.hospital).select_related("doctor")

    @staticmethod
    def change_reset_password(request, data):
        action = data.get("action")
        password_id = data.get("password_id")
        password = data.get("password")
        if password_id and action:
            doctor_obj = ResetPasswordRequest.objects.filter(id=password_id, status="REQUESTED")
            if action == "approve" and doctor_obj:
                doctor_obj[0].doctor.password = password
                doctor_obj[0].status = "APPROVED"
                doctor_obj[0].doctor.save()
                doctor_obj[0].save()
            else:
                doctor_obj[0].status = "CANCELLED"
                doctor_obj[0].save()
        else:
            raise Exception('You are missing something')
    @staticmethod
    def fetch_doctor_leave_requests(request, data):
        return DoctorLeave.objects.filter(doctor__hospital_id=request.user.hospital).select_related("doctor")


    @staticmethod
    def leave_request_action(request, data):
        action = data.get("action", False)
        id = data.get("id")
        doc_obj = DoctorLeave.objects.filter(id=id)
        if doc_obj:
            if action == "Approve":
                doc_obj[0].status = "APPROVED"
                doc_obj[0].doctor.is_active = False
                doc_obj[0].doctor.save()
                req_appointment = Appointment.objects.filter(date_appointment__lte=doc_obj[0].to_date, date_appointment__gte=doc_obj[0].from_date, doctor=doc_obj[0].doctor, status="pending")
                for range in req_appointment:
                    range.status = "cancel"
                    range.payment_status = "Refund"
                    range.cancel_reason = "Appointment cancelled by hospital"
                    if range.razorpay_payment_id:
                        try:
                            if range.razorpay_payment_id:
                                razorpay_client.payment.refund(range.razorpay_payment_id)
                        except:
                            pass
                    range.save()
            else:
                doc_obj[0].doctor.is_active = True
                doc_obj[0].doctor.save()

                doc_obj[0].status = "REJECTED"
            doc_obj[0].save()


    @staticmethod
    @transaction.atomic
    def add_new_doctor_hospital(request, data):
        hospital_id = request.user.hospital
        hospital_admin_id = data.get("HospitalsId", False)
        if hospital_admin_id:
            hospital_id = hospital_admin_id
        full_name = data.get("fullName", None)
        email = data.get("email", None)
        phone = data.get("phoneNumber", None)
        department = data.get("department", None)
        education = data.get("education", None)
        address = data.get("address", None)
        experience = data.get("experience", None)
        specialization = data.get("specialization", None)
        profilePhoto = data.get("profilePhoto", None)
        bio = data.get("bio", None)
        morningPrice = data.get("morningPrice", None)
        afternoonPrice = data.get("afternoonPrice", None)
        eveningPrice = data.get("eveningPrice", None)
        morningSlots = data.get("morningSlots", None)
        afternoonSlots = data.get("afternoonSlots", None)
        eveningSlots = data.get("eveningSlots", None)
        morningTime = data.get("morningTime", None)
        eveningTime = data.get("eveningTime", None)
        afternoonTime = data.get("afternoonTime", None)
        license = data.get("license", None)
        hospital_details = HospitalAdmin.objects.get(hospital_id=hospital_id)
        latest_ujur_id = False
        new_id_to_add = ""
        if hospital_id:
            try:
                latest_hospital_admin = doctorDetails.objects.filter(hospital_id=hospital_id).latest('id')
                latest_ujur_id = latest_hospital_admin.ujur_id
            except doctorDetails.DoesNotExist:
                new_id_to_add = hospital_details.ujur_id + "D1"
            if latest_ujur_id:
                reversed_s = latest_ujur_id[::-1]
                d_index = reversed_s.index('D')
                number_reversed = reversed_s[:d_index]
                number = int(number_reversed[::-1])
                number += 1
                new_id_to_add = hospital_details.ujur_id + "D" + str(number)
            else:
                new_id_to_add = hospital_details.ujur_id + "D1"
        if hospital_id:
            user = UsersDetails.objects.create(email=email,phone=phone)
            slots = False
            if morningTime and morningSlots and morningPrice:
                slots = True
            elif afternoonTime and afternoonSlots and afternoonPrice:
                slots = True
            elif eveningTime and eveningSlots and eveningPrice:
                slots = True
            if slots:
                doctor_obj = doctorDetails.objects.create(
                    ujur_id=new_id_to_add,
                    user=user,
                    email=email,
                    password="demo@123",
                    full_name=full_name,
                    bio=bio,
                    department_id=department,
                    education=education,
                    address=address,
                    experience=experience,
                    profile_picture=profilePhoto,
                    hospital_id=hospital_id,
                    specialization=specialization
                )
                doctorSlots.objects.create(
                doctor=doctor_obj,
                medical_license=license,
                morning_timings=morningTime,
                afternoon_timings=afternoonTime,
                evening_timings=eveningTime,
                morning_slots=morningSlots,
                afternoon_slots=afternoonSlots,
                evening_slots=eveningSlots,
                morning_slots_price=morningPrice,
                afternoon_slots_price=afternoonPrice,
                evening_slots_price=eveningPrice
                )
                return doctor_obj
            else:
                raise Exception("Slots, Timings and Price is Mandatory")

    @staticmethod
    @transaction.atomic
    def add_new_admin_doctor_hospital(request, data):
        hospital_admin_id = data.get("HospitalsId", False)
        hospital_id=False
        if hospital_admin_id:
            hospital_id = hospital_admin_id
        full_name = data.get("fullName", None)
        email = data.get("email", None)
        phone = data.get("phoneNumber", None)
        department = data.get("department", None)
        education = data.get("education", None)
        address = data.get("address", None)
        experience = data.get("experience", None)
        specialization = data.get("specialization", None)
        profilePhoto = data.get("profilePhoto", None)
        bio = data.get("bio", None)
        morningPrice = data.get("morningPrice", None)
        afternoonPrice = data.get("afternoonPrice", None)
        eveningPrice = data.get("eveningPrice", None)
        morningSlots = data.get("morningSlots", None)
        afternoonSlots = data.get("afternoonSlots", None)
        eveningSlots = data.get("eveningSlots", None)
        morningTime = data.get("morningTime", None)
        eveningTime = data.get("eveningTime", None)
        afternoonTime = data.get("afternoonTime", None)
        license = data.get("license", None)
        hospital_details = HospitalAdmin.objects.get(hospital_id=hospital_id)
        latest_ujur_id = False
        if hospital_id:
            try:
                latest_hospital_admin = doctorDetails.objects.filter(hospital_id=hospital_id).latest('id')
                latest_ujur_id = latest_hospital_admin.ujur_id
            except doctorDetails.DoesNotExist:
                new_id_to_add = hospital_details.ujur_id + "D1"
            if latest_ujur_id:
                reversed_s = latest_ujur_id[::-1]
                d_index = reversed_s.index('D')
                number_reversed = reversed_s[:d_index]
                number = int(number_reversed[::-1])
                number += 1
                new_id_to_add = hospital_details.ujur_id + "D" + str(number)
            else:
                new_id_to_add = hospital_details.ujur_id + "D1"
            user = UsersDetails.objects.create(email=email,phone=phone)
            doctor_obj = doctorDetails.objects.create(
                ujur_id=new_id_to_add,
                user = user,
                email = email,
                password = "demo@123",
                full_name = full_name,
                bio =bio,
                department_id=department,
                education=education,
                address=address,
                experience=experience,
                profile_picture=profilePhoto,
                hospital_id=hospital_id,
                specialization=specialization
            )
            doctor_slots = doctorSlots.objects.create(
                doctor=doctor_obj,
                medical_license=license,
                morning_timings=morningTime,
                afternoon_timings=afternoonTime,
                evening_timings=eveningTime,
                morning_slots=morningSlots,
                afternoon_slots=afternoonSlots,
                evening_slots=eveningSlots,
                morning_slots_price=morningPrice,
                afternoon_slots_price=afternoonPrice,
                evening_slots_price=eveningPrice,
            )

        return doctor_obj

    @staticmethod
    def edit_doctor_hospital(request, data):
        doctor_id = data.get("doctor_id", None)
        full_name = data.get("fullName", None)
        email = data.get("email", None)
        department = data.get("department", None)
        education = data.get("education", None)
        address = data.get("address", None)
        experience = data.get("experience", None)
        specialization = data.get("specialization", None)
        profilePhoto = data.get("profilePhoto", None)
        bio = data.get("bio", None)
        morningPrice = data.get("morningPrice", None)
        afternoonPrice = data.get("afternoonPrice", None)
        eveningPrice = data.get("eveningPrice", None)
        morningSlots = data.get("morningSlots", None)
        afternoonSlots = data.get("afternoonSlots", None)
        eveningSlots = data.get("eveningSlots", None)
        morningTime = data.get("morningTime", None)
        eveningTime = data.get("eveningTime", None)
        afternoonTime = data.get("afternoonTime", None)
        phone_number = data.get("phoneNumber")

        if doctor_id:
            doctor_obj = doctorDetails.objects.get(id=doctor_id)
            if email:
                doctor_obj.email = email
            if phone_number:
                doctor_obj.user.phone = phone_number
                doctor_obj.user.save()
            if full_name:
                doctor_obj.full_name = full_name
            if bio:
                doctor_obj.bio =bio
            if department:
                doctor_obj.department_id = department
            if education:
                doctor_obj.education = education
            if address:
                doctor_obj.address = address
            if experience:
                doctor_obj.experience = experience
            if profilePhoto:
                doctor_obj.profile_picture = profilePhoto
            if specialization:
                doctor_obj.specialization = specialization
            doctor_obj.save()
            doctor_slots = doctorSlots.objects.get(doctor_id=doctor_id)
            if morningTime:
                doctor_slots.morning_timings = morningTime
            if afternoonTime:
                doctor_slots.afternoon_timings = afternoonTime
            if eveningTime:
                doctor_slots.evening_timings = eveningTime
            if morningSlots:
                doctor_slots.morning_slots = morningSlots
            if afternoonSlots:
                doctor_slots.afternoon_slots = afternoonSlots
            if eveningSlots:
                doctor_slots.evening_slots = eveningSlots
            if morningPrice:
                doctor_slots.morning_slots_price = morningPrice
            if afternoonPrice:
                doctor_slots.afternoon_slots_price = afternoonPrice
            if eveningPrice:
                doctor_slots.evening_slots_price = eveningPrice
            doctor_slots.save()

        return doctor_obj

    @staticmethod
    def reset_password_request_apply(request, data):
        email_to_reset = data.get("email")
        if email_to_reset:
            doctor = doctorDetails.objects.filter(ujur_id=email_to_reset)
            if doctor:
                ResetPasswordRequest.objects.create(doctor=doctor[0])
        else:
            raise Exception("You are missing something")


    @staticmethod
    def fetch_all_software_departments(request, data):
        return Department.objects.filter()

    @staticmethod
    @transaction.atomic
    def add_hospital_department(request, data):
        department_id = data.get("departmentId")
        department_name = data.get("departmentName")
        department_description = data.get("departmentComments")
        if department_id and department_id != "new":
            check_prev = DepartmentHospitalMapping.objects.filter(department_id=department_id,hospital_id=request.user.hospital)
            if check_prev:
                raise Exception("This department already exists")
            DepartmentHospitalMapping.objects.create(
                department_id=department_id,
                hospital_id=request.user.hospital
            )
        if department_name and department_description:
            department_id = Department.objects.create(
                name=department_name,
                description=department_description
            )
            DepartmentHospitalMapping.objects.create(
                department=department_id,
                hospital_id=request.user.hospital
            )

    @staticmethod
    @transaction.atomic
    def add_hospital_admin(request, data):
        department_name = data.get("departmentName")
        department_description = data.get("departmentComments", None)
        if department_name:
            Department.objects.create(
                name=department_name,
                description=department_description
            )
        else:
            raise Exception("Department Name and Description is compulsory")

    @staticmethod
    def get_all_reviews(request, data):
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        hospitals = data.get('hospitalSearch', False)
        department = data.get('department', False)
        filters = Q()
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if hospitals:
            filters &= Q(doctor__hospital=hospitals)
        if department:
            filters &= Q(doctor__department=department)
        return PatientDoctorReviews.objects.filter(filters).select_related("patient")

    @staticmethod
    def get_all_hospital_reviews(request, data):
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        hospitals = data.get('hospitalSearch', False)
        department = data.get('department', False)
        star_review = data.get('starSearch', False)
        date = data.get('date', False)

        filters = Q(doctor__hospital_id=request.user.hospital)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if hospitals:
            filters &= Q(doctor__hospital=hospitals)
        if star_review:
            filters &= Q(reviews_star=star_review)
        if date:
            filters &= Q(created_at__date=date)
        return PatientDoctorReviews.objects.filter(filters).select_related("patient","doctor", "doctor__hospital", "doctor__department").order_by("-created_at")


    @staticmethod
    def change_doctor_profile(request, data):
        profile_picture = data.get("profilePhoto", False)
        sign_picture = data.get("signPhoto", False)
        if profile_picture or sign_picture:
            doctor_obj = doctorDetails.objects.get(id=request.user.doctor)
            if profile_picture:
                doctor_obj.profile_picture = profile_picture
            if sign_picture:
                doctor_obj.signature = sign_picture
            doctor_obj.save()
        else:
            raise Exception("One photo should be uploaded")

    @staticmethod
    def fetch_token_refersh(request, data):
        return doctorDetails.objects.select_related("hospital").get(id=request.user.doctor)


    @staticmethod
    def fetch_medicines_doctor(request, data):
        doctor_details = doctorDetails.objects.get(id=request.user.doctor)
        return MedicinesName.objects.filter(hospital=doctor_details.hospital)

    @staticmethod
    def add_medicines_doctor(request, data):
        doctor_details = doctorDetails.objects.get(id=request.user.doctor)
        medicines_name = data.get("name")
        medicines_description = data.get("description", None)
        if medicines_name:
            return MedicinesName.objects.create(
                hospital=doctor_details.hospital,
                name = medicines_name,
                description = medicines_description
            )
    @staticmethod
    @transaction.atomic
    def add_reviews_patient(request, data):
        appointmentId = data.get("appointmentId")
        rating = data.get("rating")
        comment = data.get("comment", None)
        if appointmentId and rating:
            appointment_old = Appointment.objects.get(id=appointmentId)
            get_old_review = PatientDoctorReviews.objects.filter(patient_id=request.user.id, doctor_id=appointment_old.doctor_id)
            if get_old_review:
                get_old_review[0].reviews_star = rating
                get_old_review[0].comment = comment
                get_old_review[0].save()
            else:
                PatientDoctorReviews.objects.create(patient_id=request.user.id, doctor_id=appointment_old.doctor_id,reviews_star=rating, comment=comment )
        else:
            raise Exception("Something went Wrong")

    @staticmethod
    def check_reviews_patient(request, data):
        appointmentId = data.get("appointmentId")
        if appointmentId:
            appointment_old = Appointment.objects.get(id=appointmentId)
            get_old_review = PatientDoctorReviews.objects.filter(patient_id=request.user.id, doctor_id=appointment_old.doctor_id)
            return get_old_review[0]

        else:
            raise Exception("Something went Wrong")

    @staticmethod
    @transaction.atomic
    def add_reviews_patient_hospital(request, data):
        appointmentId = data.get("appointmentId")
        rating = data.get("rating")
        comment = data.get("comment", None)
        if appointmentId and rating:
            appointment_old = Appointment.objects.get(id=appointmentId)
            get_old_review = HospitalPatientReviews.objects.filter(patient_id=request.user.id, hospital_id=appointment_old.doctor.hospital_id)
            if get_old_review:
                get_old_review[0].reviews_star = rating
                get_old_review[0].comment = comment
                get_old_review[0].save()
            else:
                HospitalPatientReviews.objects.create(patient_id=request.user.id, hospital_id=appointment_old.doctor.hospital_id,reviews_star=rating, comment=comment )
        else:
            raise Exception("Something went Wrong")

    @staticmethod
    def check_reviews_patient_hospital(request, data):
        appointmentId = data.get("appointmentId", False)
        if appointmentId:
            appointment_old = Appointment.objects.get(id=appointmentId)
            get_old_review = HospitalPatientReviews.objects.filter(patient_id=request.user.id, hospital_id=appointment_old.doctor.hospital_id)
            if get_old_review:
                return get_old_review[0]
            return []

        else:
            raise Exception("Something went Wrong")
    @staticmethod
    def fetch_hospital_department(request, data):
        try:
            req_doctor = doctorDetails.objects.get(id=request.user.doctor)
            departments_id_tuples = DepartmentHospitalMapping.objects.filter(hospital_id=req_doctor.hospital).values_list("department")
            if departments_id_tuples:
                departments_id = [dept[0] for dept in departments_id_tuples]
                department_names = Department.objects.filter(id__in = list(departments_id)).order_by("-created_at")
            return department_names
        except Exception as e:
            raise Exception("Something went Wrong")

    @staticmethod
    def get_graph_gender_age(request, data):
        timeframe = data.get("time")
        today = now().date()
        male_data = []
        female_data = []

        if timeframe == 'Week':
            # Get the Monday of the current week
            start_date = today - timedelta(days=today.weekday())
            date_range = [start_date + timedelta(days=i) for i in range(7)]
            for start in date_range:
                end = start  # Each day in the week
                male_count = Appointment.objects.filter(
                    date_appointment__date=start,
                    patient__gender='M',
                    doctor__hospital_id=request.user.hospital

                ).count()
                female_count = Appointment.objects.filter(
                    date_appointment__date=start,
                    patient__gender='F',
                    doctor__hospital_id=request.user.hospital

                ).count()
                male_data.append(male_count)
                female_data.append(female_count)

        elif timeframe == 'Month':
            start_date = today.replace(day=1)
            date_range = [
                (start_date + timedelta(days=0), start_date + timedelta(days=8)),
                (start_date + timedelta(days=9), start_date + timedelta(days=15)),
                (start_date + timedelta(days=16), start_date + timedelta(days=23)),
                (start_date + timedelta(days=24), start_date + timedelta(days=30))
            ]

            for start, end in date_range:
                male_count = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__gender='M',
                    doctor__hospital_id=request.user.hospital

                ).count()

                female_count = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__gender='F',
                    doctor__hospital_id=request.user.hospital

                ).count()

                male_data.append(male_count)
                female_data.append(female_count)

        elif timeframe == 'Year':
            start_date = today.replace(month=1, day=1)
            date_range = [(start_date.replace(month=i + 1),
                           (start_date.replace(month=i + 2) - timedelta(days=1)) if i < 11 else start_date.replace(
                               year=start_date.year + 1, month=1, day=1) - timedelta(days=1)) for i in range(12)]
            for start, end in date_range:
                male_count = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__gender='M',
                    doctor__hospital_id=request.user.hospital

                ).count()
                female_count = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__gender='F',
                    doctor__hospital_id=request.user.hospital

                ).count()
                male_data.append(male_count)
                female_data.append(female_count)

        return {"male_data": male_data, "female_data": female_data}



    @staticmethod
    def get_graph_age(request, data):
        timeframe = data.get("age")
        today = now().date()
        age_append_list_1st = []
        age_append_list_2nd = []
        age_append_list_3rd = []
        list_to_send = []
        seventeen = today.replace(year=today.year - 15) + timedelta(days=1)
        fifty = today.replace(year=today.year - 60) + timedelta(days=1)
        if timeframe == 'Week':
            start_date = today - timedelta(days=today.weekday())
            date_range = [start_date + timedelta(days=i) for i in range(7)]
            for start in date_range:
                firstPhase = Appointment.objects.filter(
                    date_appointment__date=start,
                    patient__date_of_birth__gt=seventeen,
                    doctor__hospital_id=request.user.hospital
                ).count()
                secondPhase = Appointment.objects.filter(
                    date_appointment__date=start,
                    patient__date_of_birth__gt=fifty,
                    patient__date_of_birth__lt=seventeen,
                    doctor__hospital_id=request.user.hospital
                ).count()
                thirdPhase = Appointment.objects.filter(
                    date_appointment__date=start,
                    patient__date_of_birth__lt=fifty,
                    doctor__hospital_id=request.user.hospital

                ).count()
                age_append_list_1st.append(firstPhase)
                age_append_list_2nd.append(secondPhase)
                age_append_list_3rd.append(thirdPhase)

        elif timeframe == 'Month':
            start_date = today.replace(day=1)
            date_range = [
                (start_date + timedelta(days=0), start_date + timedelta(days=8)),
                (start_date + timedelta(days=9), start_date + timedelta(days=15)),
                (start_date + timedelta(days=16), start_date + timedelta(days=23)),
                (start_date + timedelta(days=24), start_date + timedelta(days=30))
            ]

            for start, end in date_range:
                firstPhase = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__date_of_birth__gt=seventeen,
                    doctor__hospital_id=request.user.hospital
                ).count()
                secondPhase = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__date_of_birth__gt=fifty,
                    patient__date_of_birth__lt=seventeen,
                    doctor__hospital_id=request.user.hospital

                ).count()
                thirdPhase = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__date_of_birth__lt=fifty,
                    doctor__hospital_id=request.user.hospital

                ).count()
                age_append_list_1st.append(firstPhase)
                age_append_list_2nd.append(secondPhase)
                age_append_list_3rd.append(thirdPhase)
        elif timeframe == 'Year':
            start_date = today.replace(month=1, day=1)
            date_range = [(start_date.replace(month=i + 1),
                           (start_date.replace(month=i + 2) - timedelta(days=1)) if i < 11 else start_date.replace(
                               year=start_date.year + 1, month=1, day=1) - timedelta(days=1)) for i in range(12)]
            for start, end in date_range:
                firstPhase = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__date_of_birth__gt=seventeen,
                    doctor__hospital_id=request.user.hospital
                ).count()
                secondPhase = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__date_of_birth__gt=fifty,
                    patient__date_of_birth__lt=seventeen,
                    doctor__hospital_id=request.user.hospital

                ).count()
                thirdPhase = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    patient__date_of_birth__lt=fifty,
                    doctor__hospital_id=request.user.hospital

                ).count()
                age_append_list_1st.append(firstPhase)
                age_append_list_2nd.append(secondPhase)
                age_append_list_3rd.append(thirdPhase)

        return {
            "before_16": age_append_list_1st,
            "fifteen_60": age_append_list_2nd,
            "after_60": age_append_list_3rd,

        }


    @staticmethod
    def change_appointment_status_to_queue(request, data):
        appointmentId = data.get("appointmentId")
        if appointmentId:
            appointment_old = Appointment.objects.get(id=appointmentId)
            appointment_old.status = "queue"
            appointment_old.save()
        else:
            raise Exception("Something went Wrong")


    @staticmethod
    def get_completed_appointment_graph(request, data):
        doctor_id = data.get("doctorId")
        timeframe = data.get("time")
        today = now().date()
        completed_count = []
        female_data = []

        if timeframe == 'week':
            # Get the Monday of the current week
            start_date = today - timedelta(days=today.weekday())
            date_range = [start_date + timedelta(days=i) for i in range(7)]
            for start in date_range:
                end = start  # Each day in the week
                male_count = Appointment.objects.filter(
                    date_appointment__date=start,
                    doctor_id=doctor_id,
                    doctor__hospital_id=request.user.hospital
                ).count()
                completed_count.append(male_count)

        elif timeframe == 'month':
            start_date = today.replace(day=1)
            date_range = [
                (start_date + timedelta(days=0), start_date + timedelta(days=8)),
                (start_date + timedelta(days=9), start_date + timedelta(days=15)),
                (start_date + timedelta(days=16), start_date + timedelta(days=23)),
                (start_date + timedelta(days=24), start_date + timedelta(days=30))
            ]

            for start, end in date_range:
                male_count = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    doctor_id=doctor_id,
                    doctor__hospital_id=request.user.hospital
                ).count()


                completed_count.append(male_count)

        elif timeframe == 'year':
            start_date = today.replace(month=1, day=1)
            date_range = [(start_date.replace(month=i + 1),
                           (start_date.replace(month=i + 2) - timedelta(days=1)) if i < 11 else start_date.replace(
                               year=start_date.year + 1, month=1, day=1) - timedelta(days=1)) for i in range(12)]
            for start, end in date_range:
                male_count = Appointment.objects.filter(
                    date_appointment__date__range=(start, end),
                    doctor_id=doctor_id,
                    doctor__hospital_id=request.user.hospital
                ).count()
                completed_count.append(male_count)

        return completed_count

    @staticmethod
    def old_appointment_check_book(request, data):
        patient_id = request.user.id
        doctor_id = data.get("doctorId")
        date = data.get("date")
        slot = data.get("slot")

        if patient_id and doctor_id and date and slot:
            check_if_already_exist = Appointment.objects.filter(
                patient_id=patient_id,
                doctor_id=doctor_id,
                slot=slot,
                date_appointment=date,
            ).exclude(status="created")
            if check_if_already_exist:
                raise Exception("The appointment is already booked in this slot.")

    @staticmethod
    def doctor_prescription_mode_change(request, data):
        doctor_id = request.user.doctor
        method = data.get("method")
        if not method or not doctor_id or method not in ["digital" , "manual"]:
            raise Exception("There is some issue while changing the method")
        req_doctor = doctorDetails.objects.select_related("hospital").get(id=doctor_id)
        req_doctor.prescription_mode = method
        req_doctor.save()
        return req_doctor

    @staticmethod
    def get_cheif_query(request):
        chief_query = getChiefQuery.objects.filter().order_by("-created_at")
        lab_tests = labTests.objects.filter().order_by("-created_at")
        return chief_query , lab_tests

    @staticmethod
    def add_new_cheif_query(request, data):
        new_label = data.get("label")
        if not new_label:
            raise Exception("There is a error while adding the new label")
        chief_query = getChiefQuery.objects.create(value=new_label, label=new_label)
        return chief_query

    @staticmethod
    def get_lab_tests(request):
        lab_Test = labTests.objects.filter()
        return lab_Test

    @staticmethod
    def change_lab_tests(request, data):
        new_label = data.get("label")
        lab_Test = labTests.objects.create(
            label=new_label,
            value=new_label
        )
        return lab_Test

    @staticmethod
    @transaction.atomic
    def add_doctor_department(request, data):
        doctor = doctorDetails.objects.filter(id=request.user.doctor)[0]
        department_name = data.get("label")
        if not department_name:
            raise Exception("There is a error in the department name")
        if department_name:
            department_id = Department.objects.create(
                name=department_name,
                description=department_name
            )
            DepartmentHospitalMapping.objects.create(
                department=department_id,
                hospital_id=doctor.hospital.id
            )
            return True
        return False