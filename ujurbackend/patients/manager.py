from django.db import IntegrityError, transaction
from django.db.models import Q
import json
import datetime

from admin_hospital.models import promoCodes
from doctors.models import PatientDoctorReviews, HospitalPatientReviews, Appointment
from patients.models import Patient
from users.models import UsersDetails
import razorpay
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class PatientManager:
    @staticmethod
    @transaction.atomic
    def patient_signup(requests, data):
        try:
            profile_photo = data.get("document")
            phone_number = data.get("phoneNumber")
            password = data.get("password")
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            gender = data.get("gender")
            email = data.get("email", False)
            date_of_birth = data.get("dob")
            weight = data.get("weight", None)
            height = data.get("height", None)
            district = data.get("district")
            block = data.get("block")
            if phone_number and first_name and last_name and gender and date_of_birth and district and block:
                query_for_check = Q()
                query_for_check &= Q(phone=phone_number)
                if len(email):
                    query_for_check &= Q(email=email)
                user_check = UsersDetails.objects.filter(query_for_check)
                if user_check:
                    raise Exception("This Phone number or Emails already exists")
                user = UsersDetails.objects.create(phone=phone_number, email=email,password=password, role="patient")
                if email:
                    user.email = email
                    user.save()
                latest_patient = Patient.objects.latest('id')
                latest_ujur_id = latest_patient.ujur_id
                if latest_ujur_id:
                    numeric_part = int(latest_ujur_id[4:])

                    # Increment the numeric part
                    new_numeric_part = numeric_part + 1

                    # Construct the new ujur_id
                    new_id_to_add = f'UJUR{new_numeric_part}'
                else:
                    new_id_to_add = "UJUR101"
                new_patient = Patient.objects.create(
                    ujur_id=new_id_to_add,
                    user=user,
                    full_name=str(first_name) + " "+str(last_name),
                    gender=gender,
                    date_of_birth=date_of_birth,
                    district=district,
                    block=block,
                    weight=weight,
                    height=height
                )
                if profile_photo:
                    new_patient.profile_picture = profile_photo
                    new_patient.save()
                return new_patient
            else:
                raise Exception("All fields mentioned are compulsory")
        except IntegrityError as e:
            raise Exception (f"IntegrityError: {e}")

    @staticmethod
    def get_patient_profile(request, data):
        try:
            patient_id = request.user.id
            if patient_id:
                required_patient = Patient.objects.filter(id=patient_id).select_related('user')[0]
                if required_patient.created_by:
                    extra_patients = Patient.objects.filter(created_by=required_patient.created_by).exclude(
                        id=required_patient.id)
                    extra_patients = extra_patients.union(Patient.objects.filter(id=required_patient.created_by_id))


                else:
                    extra_patients = Patient.objects.filter(created_by=patient_id)
                return required_patient, extra_patients
        except Exception as e:
            pass

    @staticmethod
    def get_latest_appointment_patient(data):
        try:
            patient_id = data.get('patient_id')
            if patient_id:
                return Patient.objects.get(id =patient_id).select_related('user')
        except:
            pass

    @staticmethod
    @transaction.atomic
    def add_new_patient(requests, data):
        try:
            user_created = requests.user.id
            full_name = data.get("fullName")
            gender = data.get("gender")
            date_of_birth = data.get("dob")
            district = data.get("district")
            block = data.get("block")
            if not(user_created and full_name and gender and date_of_birth and district and block):
                raise Exception("All Fields are required")

            patient = Patient.objects.get(id=user_created)
            if patient.created_by:
                to_check = patient.created_by
            else:
                to_check = patient
            check_number = Patient.objects.filter(created_by=to_check).count()
            if check_number > 4:
                raise Exception("You can only create upto 5 members")
            latest_patient = Patient.objects.latest('id')
            latest_ujur_id = latest_patient.ujur_id
            if latest_ujur_id:
                numeric_part = int(latest_ujur_id[4:])

                # Increment the numeric part
                new_numeric_part = numeric_part + 1

                # Construct the new ujur_id
                new_id_to_add = f'UJUR{new_numeric_part}'
            else:
                new_id_to_add = "UJUR101"
            new_patient = Patient.objects.create(
                ujur_id=new_id_to_add,
                user=patient.user,
                full_name=full_name,
                gender=gender,
                date_of_birth=date_of_birth,
                district=district,
                block=block,
                created_by=to_check
            )
            return new_patient
        except IntegrityError as e:
            raise Exception (f"IntegrityError: {e}")

    @staticmethod
    def change_profile_user(requests, data):
        user_created = requests.user.id
        document = data.get("document", False)
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        email = data.get("email", False)
        password = data.get("password")
        phoneNumber = data.get("phoneNumber")
        gender = data.get("gender")
        date_of_birth = data.get("date_of_birth")
        blood_group = data.get("blood_group")
        weight = data.get("weight")
        district = data.get("district")
        block = data.get("block")
        height = data.get("height")
        patient = Patient.objects.get(id=user_created)
        new_patient = Patient.objects.get(id=user_created)
        new_patient.user=patient.user

        if (email or phoneNumber) and email != "":
            user_check = UsersDetails.objects.exclude(id=new_patient.user.id).filter(Q(email=email) | Q(phone=phoneNumber))
            if user_check:
                raise Exception("This Phone number or Emails already exists")
        if email == "":
            new_patient.user.email = email
        if firstName and lastName:
            new_patient.full_name = firstName + " " + lastName
        if gender:
            new_patient.gender = gender
        if block:
            new_patient.block = block

        if date_of_birth:
            new_patient.date_of_birth = date_of_birth

        if blood_group:
            new_patient.blood_group = blood_group

        if weight:
            new_patient.weight = weight

        if district:
            new_patient.district = district

        if height:
            new_patient.height = height

        if document:
            new_patient.profile_picture = document
        if email:
            new_patient.user.email = email
        if password:
            new_patient.user.password = password
        if phoneNumber:
            new_patient.user.phone = phoneNumber
        new_patient.save()
        new_patient.user.save()
        return new_patient


    @staticmethod
    def fetch_customer_reviews(request, data):
        try:
            patient_id = request.user.id
            if patient_id:
                return PatientDoctorReviews.objects.filter(patient__id =patient_id).select_related('doctor').select_related("patient")
        except:
            pass

    @staticmethod
    def fetch_customer_hospital_reviews(request, data):
        try:
            patient_id = request.user.id
            if patient_id:
                return HospitalPatientReviews.objects.filter(patient__id =patient_id).select_related('hospital').select_related("patient")
        except:
            pass
    @staticmethod
    def fetch_lab_reports_customers(request, data):
        try:
            patient_id = request.user.id
            if patient_id:
                return Appointment.objects.filter(patient__id =patient_id, lab_report__isnull=False).exclude(
                                lab_report=''
                            ).select_related('doctor').select_related('doctor__hospital')
        except:
            pass

    @staticmethod
    def upload_customer_lab_report(request, data):
        try:
            patient_id = request.user.id
            appointment_id = data.get("appointmentId", False)
            lab_report = data.get("labReport", False)
            prescription = data.get("prescription", False)
            if patient_id and appointment_id and (lab_report or prescription):
                req_appointment = Appointment.objects.get(patient__id =patient_id, id=appointment_id)
                if lab_report:
                    req_appointment.lab_report = lab_report
                    req_appointment.save()
                if prescription:

                    file_name = f"Prescription_{req_appointment.patient.full_name}_{req_appointment.id}_{datetime.datetime.now().strftime('%d-%m-%Y')}{prescription.name}"

                    req_appointment.prescription = prescription
                    req_appointment.prescription.name = file_name
                    req_appointment.save()
            else:
                raise Exception("No file uploaded")
        except:
            raise Exception("No file uploaded")

    @staticmethod
    def apply_coupons(request, data):
        try:
            coupon = data.get("coupon", False)
            if coupon:
                req_appointment = promoCodes.objects.filter(promocode =coupon)
                if req_appointment:
                    return req_appointment[0].percentage
                else:
                    return False
        except:
            raise Exception("Something went wrong")

    @staticmethod
    def fetch_payment_razorpay(request, data):
        try:
            amount = data.get("amount")
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            DATA = {
                "amount": int(float(amount)*100),
                "currency": "INR",
                "receipt": "receipt#1",
            }
            req_order = client.order.create(data=DATA)
            return req_order
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def verify_payment_check(request, data):
        try:
            bookingId = data.get("bookingId")
            data = data['data']
            json_string = json.loads(data)
            razorpay_order_id = json_string['response'].get("razorpay_order_id")
            razorpay_payment_id = json_string['response'].get("razorpay_payment_id")
            razorpay_signature = json_string['response'].get("razorpay_signature")
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            required_appointment = Appointment.objects.get(id=bookingId)
            try:
                verify_payment = client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                })
                required_appointment.razorpay_payment_id = razorpay_payment_id
                required_appointment.save()
            except:
                verify_payment = False
            return verify_payment
        except:
            raise Exception("Something went wrong")

    @staticmethod
    def cancel_patient_appointment(request, data):
        try:
            patient_id = request.user.id
            appointment_id = data.get("appointmentId")
            reason = data.get("reason")
            if patient_id and appointment_id and reason:
                req_appointment =  Appointment.objects.filter(patient__id =patient_id, id=appointment_id )
                if req_appointment and req_appointment[0].status != "cancel":
                    req_appointment[0].status = "cancel"
                    req_appointment[0].payment_status = "Refund"
                    req_appointment[0].cancel_reason=reason
                    req_appointment[0].save()
                try:
                    if req_appointment[0].razorpay_payment_id:
                        razorpay_client.payment.refund(req_appointment[0].razorpay_payment_id)
                except:
                    raise Exception("Due to technical glitch We are facing some issue in refunding the payment, Please ask customer support")
            else:
                raise Exception("Something went wrong")
        except:
            pass
    @staticmethod
    def get_forgot_password_account(request, data):
        email = data.get("email")
        phone = data.get("phone")
        dob = data.get("dob")
        if email and phone and dob:
            req_user = UsersDetails.objects.filter(email =email, phone=phone, user_patient_table__date_of_birth = dob)
        else:
            raise Exception("All fields are mandatory to enter")
        if req_user:
            return req_user[0]
        else:
            raise Exception("User does not exist with the given credentials")

    @staticmethod
    def change_password(request, data):
        password = data.get("password", False)
        phone = data.get("phone", False)
        if phone and password:
            req_user = UsersDetails.objects.filter(phone="+91-"+str(phone))
        else:
            raise Exception("All fields are mandatory to enter")
        if req_user:
            req_user[0].password = password
            req_user[0].save()
        else:
            raise Exception("User does not exist with the given credentials")

