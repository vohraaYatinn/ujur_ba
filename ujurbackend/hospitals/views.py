from rest_framework.views import APIView
from rest_framework.response import Response

from admin_hospital.serializer import HospitalAdminsSerailizer, HospitalReviewsWithPatientsSerializer, \
    AppointmentWithDepartmentandDoctorWithRevenueSerializer, AppointmentWithDepartmentandDoctorHospitalSerializer
from doctors.manager import DoctorsManagement
from doctors.serializer import DoctorUserSerializer, DoctorSerializer, DoctorAverageUserSerializer, \
    resetPasswordsDoctor, LeaveSerializer, LeaveDoctorSerializer, AppointmentWithDepartmentSerializer, \
    AppointmentWithDepartmentandDoctorSerializer, DoctorReviewsSerializer, DoctorReviewsWithPatientsAndDoctorSerializer, \
    PatientDetailsFprDoctorSerializer, MedicinesSerializer, ReferToSerializer, \
    PatientDetailsFprDoctorWithEmailSerializer, PatientDetailsWithUserDoctorSerializer, AppointmentUserSerializer, \
    DoctorReviewsWithPatientsUserAndDoctorSerializer
from hospitals.manager import HospitalManager
from hospitals.serializer import HospitalSerializer, HospitalSerializerWithDoctors, LabReportsSerializer, \
    DepartmentSerializer, DepartmentMappingSerializer, DoctorModelForHospitalSerializer, HospitalWithReviewSerializer, \
    HospitalSerializerWithRatingDoctors, DoctorModelForHospitalWithDeparmentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedHospital, IsAuthenticatedAdminPanel
import jwt

from patients.manager import PatientManager


class HospitalFetchDashboard(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_data = HospitalManager.fetch_dashboard_hospital(data)
            hospital_serialized_data = HospitalWithReviewSerializer(hospital_data, many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalFetchDoco(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_doc_data = HospitalManager.fetch_doctors_hospital_patient({},data)
            hospital_serialized_data = HospitalSerializerWithRatingDoctors(hospital_doc_data).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchLabReports(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_doc_data = HospitalManager.fetch_lab_reports(request)
            hospital_serialized_data = LabReportsSerializer(hospital_doc_data, many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalAdminLogin(APIView):
    permission_classes = []
    @staticmethod
    def post(request):
        try:
            data = request.data
            hospital_login = HospitalManager.hospital_admin_login_check(data)
            if hospital_login:
                payload = {
                    'email': hospital_login.username,
                    'admin': hospital_login.id,
                    'hospital': hospital_login.hospital.id,
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
                return Response({"result": "success", "message": "Doctor login successfully", "token": token,"hospital":hospital_login.hospital.logo.url}, 200)
            else:
                return Response(
                    {"result": "failure", "message": "Please Check the Username or Password", "token": False}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class HospitalDoctors(APIView):
    permission_classes = [IsAuthenticatedHospital]
    @staticmethod
    def get(request):
        try:
            hospital_id = {}
            data = request.query_params
            hospital_id['hospitalId'] = request.user.hospital
            hospital_doc_data = HospitalManager.fetch_doctors_hospital(data, hospital_id)
            hospital_serialized_data = DoctorModelForHospitalWithDeparmentSerializer(hospital_doc_data, many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalDoctorsProfile(APIView):
    permission_classes = []
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            doctor_obj = DoctorsManagement.fetch_hospital_doctor_profile(request, data)
            doctor_serialized_data = DoctorAverageUserSerializer(doctor_obj).data

            return Response(
                {"result": "success", "data": doctor_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalAddDoctors(APIView):
    permission_classes = [IsAuthenticatedHospital]
    @staticmethod
    def post(request):
        try:
            data = request.data
            doctor_obj = DoctorsManagement.add_new_doctor_hospital(request, data)
            return Response(
                {"result": "success", "message": "New Doctor added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalEditDoctors(APIView):
    permission_classes = [IsAuthenticatedHospital]
    @staticmethod
    def post(request):
        try:
            data = request.data
            doctor_obj = DoctorsManagement.edit_doctor_hospital(request, data)
            return Response(
                {"result": "success", "message": "Doctor edited successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandlePasswordRequest(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.data
            reset_pass_obj = DoctorsManagement.fetch_reset_request(request, data)
            reset_pass_data = resetPasswordsDoctor(reset_pass_obj, many=True).data

            return Response(
                {"result": "success", "data": reset_pass_data}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            reset_pass_obj = DoctorsManagement.change_reset_password(request, data)
            return Response(
                {"result": "success", "message": "Action on the request has been made successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchDoctorLeaveRequests(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            latest_appointment = DoctorsManagement.doctor_self_appointment_fetch(request, data)
            latest_appointment_data = AppointmentWithDepartmentandDoctorSerializer(latest_appointment, many=True).data

            return Response(
                {"result": "success", "data": latest_appointment_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class FetchHospitalAppointments(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            appointment_objs = DoctorsManagement.fetch_hospital_appointments(request, data)
            latest_appointment_data = AppointmentWithDepartmentandDoctorHospitalSerializer(appointment_objs, many=True).data
            return Response(
                {"result": "success", "data": latest_appointment_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchDoctorLeaveRequests(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            latest_appointment = DoctorsManagement.doctor_leave_fetch(request, data)
            latest_appointment_data = LeaveDoctorSerializer(latest_appointment, many=True).data

            return Response(
                {"result": "success", "data": latest_appointment_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            latest_appointment = DoctorsManagement.leave_request_action(request, data)
            return Response(
                {"result": "success", "message": "Leave action have been performed successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class FetchHospitalDepartments(APIView):
    permission_classes = []

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            departments = HospitalManager.fetch_hospital_departments(request, data)
            departments_data = DepartmentMappingSerializer(departments, many=True).data

            return Response(
                {"result": "success", "data": departments_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchAllDepartments(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            departments = HospitalManager.fetch_all_admin_departments(data)
            departments_data = DepartmentSerializer(departments, many=True).data

            return Response(
                {"result": "success", "data": departments_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.add_department_hospital(request, data)
            return Response(
                {"result": "success", "message": "Action has been performed successfully"}, 200)

        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class FetchHospitalReviews(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            reviews = DoctorsManagement.hospital_reviews(request, data)
            reviews_serialized_data = DoctorReviewsWithPatientsAndDoctorSerializer(reviews).data
            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchPatientsAdmin(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_patients = DoctorsManagement.all_patients_admin(request, data)
            reviews_serialized_data = PatientDetailsWithUserDoctorSerializer(all_patients, many=True).data
            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class AddHospitalAdmin(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.add_admin_hospital(request, data)
            return Response({"result" : "success", "message": "Hospital Admin Added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchPatientsHospitals(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_patients = DoctorsManagement.all_patients_hospital(request, data)
            reviews_serialized_data = PatientDetailsWithUserDoctorSerializer(all_patients, many=True).data
            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class AddPatientsHospitals(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def post(request):
        try:
            data = request.data
            all_patients = DoctorsManagement.add_patients_hospital(request, data)
            return Response({"result" : "success", "message": "Patient Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class GetSoftwareDepartments(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.data
            get_departments = DoctorsManagement.fetch_all_software_departments(request, data)
            reviews_serialized_data = DepartmentSerializer(get_departments, many=True).data

            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class AddDepartmentsHospitals(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def post(request):
        try:
            data = request.data
            all_patients = DoctorsManagement.add_hospital_department(request, data)
            return Response({"result" : "success", "message": "New Department Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class AddDepartmentsAdmin(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.add_hospital_admin(request, data)
            return Response({"result" : "success", "message": "New Department Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchAllReviews(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_reviews = DoctorsManagement.get_all_reviews(request, data)
            reviews_serialized_data = DoctorReviewsWithPatientsUserAndDoctorSerializer(all_reviews, many=True).data

            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandleDeleteHospital(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = HospitalManager.handle_delete_hospital(data)
            return Response({"result" : "success", "message": "Hospital Admin deleted successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandleDoctors(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_id = request.user.hospital
            doctor = HospitalManager.fetch_each_doctors_hospital(hospital_id)
            hospital_serialized_data = DoctorModelForHospitalWithDeparmentSerializer(doctor, many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandleDepartments(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            department_id = HospitalManager.fetch_hospital_departments(request, data).values_list('department_id', flat=True)
            departments = HospitalManager.get_departments(department_id)
            departments_data = DepartmentSerializer(departments, many=True).data
            return Response({"result" : "success","data": departments_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalDoctorReviews(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_reviews = DoctorsManagement.get_all_hospital_reviews(request, data)
            reviews_serialized_data = DoctorReviewsWithPatientsAndDoctorSerializer(all_reviews, many=True).data
            return Response({"result" : "success","data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandleHospitalAdmins(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            admin = HospitalManager.fetch_hospital_admin_data(request, data)
            admin_serialized_data = HospitalAdminsSerailizer(admin,many=True).data
            return Response({"result" : "success", "data": admin_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = HospitalManager.add_hospital_admin_data(request, data)
            return Response({"result" : "success", "message": "Hospital Admin added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class handleHospitalMedicines(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            medicine_data = HospitalManager.fetch_medicines_hospital(request, data)
            medicine_data_serialized = MedicinesSerializer(medicine_data, many=True).data
            return Response({ "result": "success", "data": medicine_data_serialized }, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.add_medicines_hospital(request, data)
            return Response({"result": "success", "message": "Medicine Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class handleReferToMedicines(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            refer_data = HospitalManager.fetch_refer_to_hospital(request, data)
            refer_data_serialized = ReferToSerializer(refer_data, many=True).data
            return Response({ "result": "success", "data": refer_data_serialized }, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.add_refer_to_hospital(request, data)
            return Response({"result": "success", "message": "Medicine Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class cancelAppointments(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            HospitalManager.delete_hospital_admin(request, data)
            return Response({"result": "success", "message": "Appointment Deleted Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class uploadLabReport(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.upload_lab_report(request, data)
            return Response({"result": "success", "message": "Lab Report Uploaded Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class deleteHospitalAdmin(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.delete_hospital_admin(request, data)
            return Response({"result": "success", "message": "Admin Deleted Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class hospitalAnalyticsGraphs(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            data_check = HospitalManager.analytics_graphs_hospital(request, data)
            return Response({"result": "success", "message": "Lab Report Uploaded Successfully", "data":data_check}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class genderGraphFetch(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            data_check = HospitalManager.gender_analytics_graphs_hospital(request, data)
            return Response({"result": "success", "message": "Lab Report Uploaded Successfully", "data":data_check}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class fetchHospitalSelfReviews(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            reviews = DoctorsManagement.self_hospital_reviews(request, data)
            reviews_serialized_data = HospitalReviewsWithPatientsSerializer(reviews, many=True).data
            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class fetchHospitalGenderAge(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            reviews = DoctorsManagement.get_graph_gender_age(request, data)
            reviews_age = DoctorsManagement.get_graph_age(request, data)
            return Response({"result" : "success", "data": reviews, "age":reviews_age}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class completeDoctorGraph(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            completed_count = DoctorsManagement.get_completed_appointment_graph(request, data)
            return Response({"result" : "success", "data": completed_count}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class ageGraphsFetch(APIView):
    permission_classes = [IsAuthenticatedHospital]
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            data_check = HospitalManager.age_analytics_graphs_hospital(request, data)
            return Response({"result": "success", "message": "Lab Report Uploaded Successfully", "data":data_check}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)



class AppointmentActionHospital(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.appointment_action_hospital(request, data)
            return Response({"result": "success", "message": "Request has been applied successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)



class FetchAllRevenueHospital(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_data = DoctorsManagement.fetch_all_revenue_hospital(request, data)
            appointment_data = AppointmentWithDepartmentandDoctorWithRevenueSerializer(hospital_data, many=True).data
            return Response({"result": "success", "data": appointment_data}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)