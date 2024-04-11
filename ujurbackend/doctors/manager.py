from sqlite3 import IntegrityError

from doctors.models import doctorDetails, doctorSlots, FavDoctors, Appointment, PatientDoctorReviews, DoctorLeave, \
    ResetPasswordRequest
from django.db.models import Avg, Count, Prefetch
from django.db.models.functions import Round
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from hospitals.models import HospitalDetails, Department, DepartmentHospitalMapping
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
    def fetch_all_appointments(data):
        filters = Q()
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        date = data.get('date', False)
        slots = data.get('slots', False)
        status = data.get('status', False)
        department = data.get('department', False)
        hospitals = data.get('hospitalSearch', False)
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
        appointments = Appointment.objects.filter(filters
        ).select_related("doctor", "patient")
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
    def all_patients_admin(request, data):
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
        patient_ids = Appointment.objects.filter(filters).values('patient').distinct()
        unique_patients = Patient.objects.filter(id__in=patient_ids)
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
        check_doctor = doctorDetails.objects.filter(email=email, password=password).select_related("hospital")
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
        doctor_leave = Appointment.objects.filter(filters).exclude(status="created").select_related("doctor").select_related("patient")
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
        while current_date <= end_of_period:
            appointments = Appointment.objects.filter(
                doctor_id=request.user.doctor,
                date_appointment=current_date.date(),
            ).values('status').annotate(count=Count('status'))

            total_count = sum(appt['count'] for appt in appointments)
            pending_count = sum(appt['count'] for appt in appointments if appt['status'] == 'pending')
            canceled_count = sum(appt['count'] for appt in appointments if appt['status'] == 'canceled')
            completed_count = sum(appt['count'] for appt in appointments if appt['status'] == 'completed')

            total.append(total_count)
            pending.append(pending_count)
            canceled.append(canceled_count)
            completed.append(completed_count)
            current_date += timedelta(days=1)

        return {
            "total": total,
            "pending": pending,
            "canceled": canceled,
            "completed": completed,
        }

    @staticmethod
    def doctor_patients_appointments(request, data):
        date = data.get('date', False)
        filters = Q(doctor_id=request.user.doctor)
        if not date:
            raise Exception("Not Date Provided")
        filters &= Q(date_appointment__date = date)
        total_appointments = Appointment.objects.filter(
            filters
        ).select_related("patient").order_by("-created_at")
        pending_appointments = Appointment.objects.filter(
            filters & Q(status="pending")
        ).select_related("patient").order_by("date_appointment")
        canceled_appointments = Appointment.objects.filter(
            filters & Q(status="canceled")
        ).select_related("patient").order_by("date_appointment")
        completed_appointments = Appointment.objects.filter(
            filters & Q(status="completed")
        ).select_related("patient").order_by("date_appointment")

        return {
            'total_appointments': total_appointments,
            'pending_appointments': pending_appointments,
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
        patient_name = data.get("patientName")
        filters = Q(doctor_id = request.user.doctor)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        appointments_with_specific_doctor = Appointment.objects.filter(filters)
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
            prefetch_value = Prefetch("patient_appointments", Appointment.objects.order_by("-date_appointment").order_by("-created_at"), to_attr="appointments")
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
        if email_to_reset:
            doctor = doctorDetails.objects.filter(email=email_to_reset)
            if doctor:
                ResetPasswordRequest.objects.create(doctor=doctor[0])
        else:
            raise Exception("You are missing something")


    @staticmethod
    def fetch_all_software_departments(request, data):
        return Department.objects.filter()

    @staticmethod
    def add_hospital_department(request, data):
        department_id = data.get("departmentId")
        department_name = data.get("departmentName")
        department_description = data.get("departmentComments")
        if department_id and department_id != "new":
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
    def add_hospital_admin(request, data):
        department_name = data.get("departmentName")
        department_description = data.get("departmentComments")
        if department_name and department_description:
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
        return Patient

    @staticmethod
    def get_all_hospital_reviews(request, data):
        patient_name = data.get('patientName', False)
        doctor_name = data.get('doctorName', False)
        hospitals = data.get('hospitalSearch', False)
        department = data.get('department', False)
        filters = Q(doctor__hospital_id=request.user.hospital)
        if patient_name:
            filters &= Q(patient__full_name__icontains = patient_name)
        if doctor_name:
            filters &= Q(doctor__full_name__icontains = doctor_name)
        if hospitals:
            filters &= Q(doctor__hospital=hospitals)
        if department:
            filters &= Q(doctor__department=department)
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