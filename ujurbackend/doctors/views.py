import jwt
from rest_framework.permissions import IsAuthenticated, IsDoctorAuthenticated, IsAuthenticatedAdminPanel
from rest_framework.views import APIView
from rest_framework.response import Response
from doctors.manager import DoctorsManagement
from doctors.serializer import DoctorSerializer, DocotrSlotsSerializer, DoctorReviewsSerializer, DoctorSingleSerializer, \
    DoctorSlotsSerializer, AppointmentSerializer, AppointmentWithDepartmentSerializer, DoctorFavSerializer, \
    AppointmentWithDoctorSerializer, DoctorReviewsWithPatientsSerializer, DoctorUserSerializer, \
    PatientDetailsWithUserDoctorSerializer, PatientAppointmentsSerializer, LeaveSerializer, \
    AppointmentWithDoctorAndPatientSerializer, DoctorModelSerializer, DoctorHospitalSerializer, MedicinesSerializer, \
    checkReviewSerializer, checkHospitalReviewSerializer
from hospitals.manager import HospitalManager
from hospitals.serializer import DepartmentSerializer


class DoctorFetchDashboard(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            doctor_data = DoctorsManagement.fetch_dashboard_doctor(data)
            doctor_serialized_data = DoctorSerializer(doctor_data, many=True).data
            return Response({"result" : "success", "data": doctor_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class DoctorFetchSingle(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            doctor_data, isFav = DoctorsManagement.fetch_single_doctor(request, data)
            doctor_serialized_data = DoctorSingleSerializer(doctor_data).data
            return Response({"result" : "success", "data": doctor_serialized_data, "fav":isFav}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class DoctorSlots(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            doctor_slots, dates_and_days = DoctorsManagement.fetch_doctor_slots(data)
            doctor_slots_serialized_data = DocotrSlotsSerializer(doctor_slots).data
            return Response({"result" : "success", "data": doctor_slots_serialized_data, "dates_and_days":dates_and_days}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FavDoctor(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            fav_doc = DoctorsManagement.fav_doctor_fetch(request, data)
            fav_doc_serializer = DoctorFavSerializer(fav_doc, many=True).data
            return Response({"result" : "success", "data": fav_doc_serializer}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.fav_doctor_select(request, data)
            return Response({"result" : "success", "message": "Doctor added to fav Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)



class DoctorReviews(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            reviews = DoctorsManagement.patient_doctor_reviews(request, data)
            reviews_serialized_data = DoctorReviewsSerializer(reviews).data
            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.patient_doctor_reviews_create(request, data)
            return Response({"result" : "success", "message": "Reviews Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchBookAppointment(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            booking_id = DoctorsManagement.patient_appointment_book(request, data)
            return Response({"result" : "success", "booking_id": booking_id}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchBookingPrice(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            price = DoctorsManagement.get_booking_price(data)
            return Response({"result" : "success", "price": price}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class bookingConfirmationAppointment(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            booking_confirm, appointment = DoctorsManagement.patient_booking_confirmation(data)
            appointment = AppointmentSerializer(appointment).data
            return Response({"result" : "success", "booking_confirm": booking_confirm, "data": appointment}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchLatestAppointment(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            latest_appointment = DoctorsManagement.fetch_patient_latest_appointment(request, data)
            latest_appointment_data = AppointmentSerializer(latest_appointment).data
            return Response({"result" : "success", "data": latest_appointment_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchAppointmentDetails(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            latest_appointment, slot, count = DoctorsManagement.fetch_appointment_details_per_appointment(data)
            latest_appointment_data = AppointmentWithDoctorAndPatientSerializer(latest_appointment).data
            slot_data = DoctorSlotsSerializer(slot).data
            return Response({"result" : "success", "data": latest_appointment_data, "slot": slot_data, "count":count}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchAppointmentDetailsPatient(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            appointment_details = DoctorsManagement.fetch_appointment_details(request, data)
            appointment_details = AppointmentWithDoctorSerializer(appointment_details, many=True).data
            return Response({"result" : "success", "data": appointment_details}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class doctorLogin(APIView):
    permission_classes = []

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            login_doctor = DoctorsManagement.login_doctor(request, data)
            if login_doctor:
                payload = {
                    'email': login_doctor.email,
                    'doctor': login_doctor.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
                doctor_serializer = DoctorHospitalSerializer(login_doctor).data
                return Response({"result": "success", "message": "Doctor login successfully", "token": token, "doctor":doctor_serializer}, 200)
            else:
                return Response({"result": "failure", "message": "Please Check the Username or Password", "token": False}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class dashboardDetails(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            dashboard_counts, time_period_dict = DoctorsManagement.doctor_dashboard_details(request, data)
            return Response(
                {"result": "success", "data": dashboard_counts, "time_period_dict":time_period_dict}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class dashboardPatientsDetails(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            appointments_data = DoctorsManagement.doctor_patients_appointments(request, data)
            total_appointment = AppointmentWithDepartmentSerializer(appointments_data['total_appointments'][:5], many=True).data
            pending_appointment = AppointmentWithDepartmentSerializer(appointments_data['pending_appointments'][:5], many=True).data
            canceled_appointment = AppointmentWithDepartmentSerializer(appointments_data['canceled_appointments'][:5], many=True).data
            completed_appointment = AppointmentWithDepartmentSerializer(appointments_data['completed_appointments'][:5], many=True).data

            return Response(
                {"result": "success", "data": {
                    'total_appointments': total_appointment,
                    'pending_appointments': pending_appointment,
                    'canceled_appointments': canceled_appointment,
                    'completed_appointments': completed_appointment,
                    'total_appointments_count': len(appointments_data['total_appointments']),
                    'pending_appointments_count': len(appointments_data['pending_appointments']),
                    'canceled_appointments_count': len(appointments_data['canceled_appointments']),
                    'completed_appointments_count': len(appointments_data['completed_appointments']),
                }}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class dashboarDoctorReviews(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            reviews_data = DoctorsManagement.doctor_fetch_reviews_top_5(request, data)
            patients_all_reviews = DoctorReviewsWithPatientsSerializer(reviews_data, many=True).data

            return Response(
                {"result": "success", "data": patients_all_reviews}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)




class doctorFetchAppointments(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            latest_appointment = DoctorsManagement.doctor_self_appointment_fetch(request, data)
            latest_appointment_data = AppointmentWithDepartmentSerializer(latest_appointment, many=True).data

            return Response(
                {"result": "success", "data": latest_appointment_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchPatientsOfDoctor(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            patients_obj = DoctorsManagement.doctor_fetch_patients(request, data)
            all_patients = PatientDetailsWithUserDoctorSerializer(patients_obj, many=True).data

            return Response(
                {"result": "success", "data": all_patients}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchDoctorReviews(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_reviews = DoctorsManagement.doctor_fetch_reviews(request, data)
            reviews_objs = DoctorReviewsWithPatientsSerializer(all_reviews['reviews_objs'], many=True).data

            return Response(
                {"result": "success", "data": {
            "star_counts": all_reviews['star_counts'],
            "average_rating": all_reviews['average_rating'],
            "reviews_objs": reviews_objs
        }}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchDoctorOwnProfile(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            doctor_obj = DoctorsManagement.fetch_my_profile_doctor(request, data)
            doctor_serialized_data = DoctorUserSerializer(doctor_obj).data

            return Response(
                {"result": "success", "data": doctor_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class doctorChangePassword(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            doctor_obj = DoctorsManagement.doctor_change_password(request, data)

            return Response(
                {"result": "success", "message": "Your Password has been changed Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class changeDoctorProfile(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            doctor_obj = DoctorsManagement.doctor_change_profile(request, data)

            return Response(
                {"result": "success", "message": "Your Profile has been updated Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchPatientProfile(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            patient_obj = DoctorsManagement.fetch_patient_profile(request, data)
            doctor_serialized_data = PatientAppointmentsSerializer(patient_obj, many=True).data
            return Response(
                {"result": "success", "data": doctor_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchPatientDocument(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            patient_obj = DoctorsManagement.patient_prescription_upload(request, data)
            return Response(
                {"result": "success", "message": "Doctor Prescription Has Been Saved Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class doctorLeaveApply(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.data
            leave_obj = DoctorsManagement.doctor_leave_get(request, data)
            leave_serializer = LeaveSerializer(leave_obj, many=True).data

            return Response(
                {"result": "success", "data": leave_serializer }, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.apply_leave(request, data)
            return Response(
                {"result": "success", "message": "Leave has been requested Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class patientSearching(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            list_to_give = DoctorsManagement.patient_searching(request, data)

            return Response(
                {"result": "success", "data": list_to_give}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class ApplyForgotPasswordRequest(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.reset_password_request_apply(request, data)
            return Response(
                {"result": "success", "message": "Reset Password Request has been applied Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class EditHospitalAdminPassword(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.edit_hospital_admin_password(request, data)
            return Response(
                {"result": "success", "message": "Password has been successfully changed"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class handleDoctorImages(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.change_doctor_profile(request, data)
            return Response(
                {"result": "success", "message": "Doctor Images Has Been Saved Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class handleDoctorTokenOnRefersh(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            login_doctor = DoctorsManagement.fetch_token_refersh(request, data)
            if login_doctor:
                payload = {
                    'email': login_doctor.email,
                    'doctor': login_doctor.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
                doctor_serializer = DoctorHospitalSerializer(login_doctor).data
                return Response({"result": "success", "message": "Doctor login successfully", "token": token, "doctor":doctor_serializer}, 200)
            else:
                return Response({"result": "failure", "message": "Please Check the Username or Password", "token": False}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class handleDoctorMedicines(APIView):
    permission_classes = [IsDoctorAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            login_doctor = DoctorsManagement.fetch_medicines_doctor(request, data)
            medicine_data = MedicinesSerializer(login_doctor, many=True).data
            return Response({ "result": "success", "data": medicine_data }, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.add_medicines_doctor(request, data)
            return Response({"result": "success", "message": "Doctor login successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class writeReview(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.add_reviews_patient(request, data)
            return Response({"result": "success", "message": "Doctoer Review Added Successfully"}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            check_reviews = DoctorsManagement.check_reviews_patient(request, data)
            review_data = checkReviewSerializer(check_reviews).data
            return Response({ "result": "success", "data": review_data }, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

class writeReviewHospital(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.add_reviews_patient_hospital(request, data)
            return Response({"result": "success", "message": "Hospital Review Added Successfully"}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

class QueuePatientAppointment(APIView):
    permission_classes = [IsDoctorAuthenticated]
    @staticmethod
    def post(request):
        try:
            data = request.data
            departments = DoctorsManagement.change_appointment_status_to_queue(request, data)
            return Response({"result": "success", "message": "Appointment Added to queue Successfully"}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class fetchDepartmentHospital(APIView):
    permission_classes = [IsDoctorAuthenticated]
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            departments = DoctorsManagement.fetch_hospital_department(request, data)
            review_data = DepartmentSerializer(departments, many=True).data
            return Response({"result": "success", "data": review_data}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

