from sqlite3 import IntegrityError

from doctors.models import doctorDetails, doctorSlots, FavDoctors, Appointment, PatientDoctorReviews, DoctorLeave, \
    ResetPasswordRequest
from django.db.models import Avg, Count, Prefetch
from django.db.models.functions import Round
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from hospitals.models import HospitalDetails
from patients.models import Patient
from users.models import UsersDetails


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
    def all_patients_hospital(request, data):
        patient_ids = Appointment.objects.values('patient').distinct()
        unique_patients = Patient.objects.filter(id__in=patient_ids)
        return unique_patients

    @staticmethod
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
    def patient_appointment_book(request, data):
        patient_id = request.user.id
        doctor_id = data.get("doctorId")
        date = data.get("date")
        slot = data.get("slot")
        comment = data.get("comment")
        bio = data.get("bio")

        if patient_id and doctor_id and date and slot:
            appointment = Appointment.objects.create(
                patient_id=patient_id,
                doctor_id=doctor_id,
                slot=slot,
                date_appointment=date,
                patients_query=comment
            )
            return appointment.id
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
    def patient_booking_confirmation(data):
        booking_id = data.get("bookingId")
        paymentMode = data.get("paymentMode")
        if booking_id:
            appointment = Appointment.objects.filter(
                id=booking_id
            ).select_related("doctor")[0]
            appointment.status = "pending"
            appointment.payment_mode = paymentMode
            appointment.save()
            return True, appointment
        else:
            raise Exception("It Looks like you have missed something, Please try again")

    @staticmethod
    def fetch_patient_latest_appointment(request, data):
        patient_id = request.user.id
        if patient_id:
            latest_appointment = Appointment.objects.filter(
                patient_id=patient_id
            ).select_related("doctor").order_by("-created_at")
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
        if patient_id and appointment_type:
            if appointment_type == "upcoming":
                appoint_type = "pending"
            else:
                appoint_type = "completed"
            latest_appointment = Appointment.objects.filter(
                patient_id=patient_id,
                status=appoint_type
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
            ).select_related("doctor").select_related("patient").order_by("-created_at")
            if latest_appointment:
                slots = doctorSlots.objects.get(doctor=latest_appointment[0].doctor)
                return latest_appointment[0], slots
            else:
                return []
        else:
            raise Exception("It Looks like you have missed something, Please try again")


    @staticmethod
    def login_doctor(request, data):
        email = data.get("email")
        password = data.get("password")
        check_doctor = doctorDetails.objects.filter(email=email, password=password)
        if check_doctor.exists():
            return check_doctor[0]
        return False

    @staticmethod
    def doctor_leave_fetch(request, data):
        doctor_leave = DoctorLeave.objects.filter(doctor__hospital_id=request.user.hospital).select_related("doctor")
        return doctor_leave

    @staticmethod
    def doctor_self_appointment_fetch(request, data):
        date = data.get("date")
        selected_date = datetime.strptime(date, "%Y-%m-%d")
        slot = data.get("slot")

        latest_appointment = Appointment.objects.filter(
            doctor_id=request.user.doctor,
            date_appointment__date=selected_date,
            slot=slot
        ).select_related("patient").select_related("doctor").exclude(status="created").order_by("-created_at")

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

    @staticmethod
    def doctor_dashboard_details(request, data):
        # Assuming the status choices are defined as constants in your model
        COMPLETED_APPOINTMENTS = 'completed'
        PENDING_APPOINTMENTS = 'pending'
        CANCELED_APPOINTMENTS = 'canceled'

        # Fetching all required statistics in one query
        appointment_stats = Appointment.objects.filter(
            doctor_id=request.user.doctor,
            date_appointment__week=timezone.now().isocalendar()[1]
        ).values('status').annotate(count=Count('status'))

        # Initializing variables with default values
        total_appointments = 0
        pending_appointments = 0
        canceled_appointments = 0

        # Extracting counts from the result
        for stat in appointment_stats:
            if stat['status'] == COMPLETED_APPOINTMENTS:
                total_appointments = stat['count']
            elif stat['status'] == PENDING_APPOINTMENTS:
                pending_appointments = stat['count']
            elif stat['status'] == CANCELED_APPOINTMENTS:
                canceled_appointments = stat['count']

        all_appointments = total_appointments + pending_appointments + canceled_appointments

        return {
            'total_appointments': total_appointments,
            'pending_appointments': pending_appointments,
            'canceled_appointments': canceled_appointments,
            'all_appointments': all_appointments,
        }


    @staticmethod
    def doctor_patients_appointments(request, data):
        latest_appointments = Appointment.objects.filter(
            doctor_id=request.user.doctor
        ).select_related("patient").order_by("-created_at")[:5]

        # Get the 5 upcoming appointments
        upcoming_appointments = Appointment.objects.filter(
            doctor_id=request.user.doctor,
            date_appointment__gte=timezone.now()
        ).select_related("patient").order_by("date_appointment")[:5]

        return {
            'latest_appointments': latest_appointments,
            'upcoming_appointments': upcoming_appointments,
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
        )[:4]

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
                "img": str(i.profile_picture)
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
        appointments_with_specific_doctor = Appointment.objects.filter(doctor_id=request.user.doctor)
        patients_with_appointments = appointments_with_specific_doctor.values_list('patient', flat=True).distinct()
        patients = Patient.objects.filter(id__in=patients_with_appointments).select_related("user")
        return patients


    @staticmethod
    def doctor_fetch_reviews(request, data):
        reviews_objs = PatientDoctorReviews.objects.filter(
            doctor_id=request.user.doctor).select_related("patient")
        # Initialize counts for each star rating
        star_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_sum = 0
        for rating_count in reviews_objs:
            star_counts[rating_count.reviews_star] = star_counts[rating_count.reviews_star] + 1
            total_sum = total_sum + rating_count.reviews_star

        return {
            "star_counts": star_counts,
            "average_rating": round(total_sum / len(reviews_objs),2),
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
            ).prefetch_related("doctor_slots").prefetch_related("doctor_reviews").select_related('user')
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
            if phone_number:
                doctor_obj[0].user.phone = phone_number
            if bio:
                doctor_obj[0].bio = bio
            doctor_obj[0].save()
        else:
            raise Exception("You are missing something")
    @staticmethod
    def fetch_patient_profile(request, data):
        patientId = data.get("patientId", False)
        if patientId:
            prefetch_value = Prefetch("patient_appointments", Appointment.objects.order_by("-date_appointment"), to_attr="appointments")
            patient_obj = Patient.objects.filter(
                id=patientId).prefetch_related(prefetch_value)
            return patient_obj
        else:
            raise Exception("You are missing something")


    @staticmethod
    def patient_prescription_upload(request, data):
        htmlContent = data.get("htmlContent", False)
        appointmentDetails = data.get("appointmentDetails", False)
        doctorComment = data.get("doctorComment", False)

        if htmlContent and appointmentDetails:
            appointment_obj = Appointment.objects.get(id=appointmentDetails)
            appointment_obj.pdf_content = htmlContent
            if doctorComment:
                appointment_obj.doctor_instruction = doctorComment
            appointment_obj.status = "completed"
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
            else:
                doc_obj[0].doctor.is_active = True
                doc_obj[0].doctor.save()

                doc_obj[0].status = "REJECTED"
            doc_obj[0].save()


    @staticmethod
    def add_new_doctor_hospital(request, data):
        hospital_id = request.user.hospital
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
        if hospital_id:
            user = UsersDetails.objects.create(email=email,phone=phone)
            doctor_obj = doctorDetails.objects.create(
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
    def reset_password_request_apply(request, data):
        email_to_reset = data.get("email")
        comment = data.get("comment")
        if email_to_reset:
            doctor = doctorDetails.objects.filter(email=email_to_reset)
            if doctor:
                ResetPasswordRequest.objects.create(doctor=doctor[0], comment=comment)
        else:
            raise Exception("You are missing something")
