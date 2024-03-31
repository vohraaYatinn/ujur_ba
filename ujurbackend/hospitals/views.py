from rest_framework.views import APIView
from rest_framework.response import Response

from doctors.manager import DoctorsManagement
from doctors.serializer import DoctorUserSerializer, DoctorSerializer, DoctorAverageUserSerializer, \
    resetPasswordsDoctor, LeaveSerializer, LeaveDoctorSerializer, AppointmentWithDepartmentSerializer, \
    AppointmentWithDepartmentandDoctorSerializer, DoctorReviewsSerializer, DoctorReviewsWithPatientsAndDoctorSerializer, \
    PatientDetailsFprDoctorSerializer
from hospitals.manager import HospitalManager
from hospitals.serializer import HospitalSerializer, HospitalSerializerWithDoctors, LabReportsSerializer, \
    DepartmentSerializer, DepartmentMappingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedHospital
import jwt

from patients.manager import PatientManager


class HospitalFetchDashboard(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_data = HospitalManager.fetch_dashboard_hospital(data)
            hospital_serialized_data = HospitalSerializer(hospital_data, many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalFetchDoco(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_doc_data = HospitalManager.fetch_doctors_hospital(data)
            hospital_serialized_data = HospitalSerializerWithDoctors(hospital_doc_data).data
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
                    'hospital': hospital_login.hospital.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
                return Response({"result": "success", "message": "Doctor login successfully", "token": token}, 200)
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
            data = {}
            data['hospitalId'] = request.user.hospital
            hospital_doc_data = HospitalManager.fetch_doctors_hospital(data)
            hospital_serialized_data = HospitalSerializerWithDoctors(hospital_doc_data).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HospitalDoctorsProfile(APIView):
    permission_classes = [IsAuthenticatedHospital]
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
            latest_appointment_data = AppointmentWithDepartmentandDoctorSerializer(appointment_objs, many=True).data
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
    permission_classes = [IsAuthenticatedHospital]

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
    permission_classes = [IsAuthenticatedHospital]

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
    permission_classes = []

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_patients = DoctorsManagement.all_patients_admin(request, data)
            reviews_serialized_data = PatientDetailsFprDoctorSerializer(all_patients, many=True).data
            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class AddHospitalAdmin(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.add_admin_hospital(request, data)
            return Response({"result" : "success", "message": "Hospital added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchPatientsHospitals(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_patients = DoctorsManagement.all_patients_hospital(request, data)
            reviews_serialized_data = PatientDetailsFprDoctorSerializer(all_patients, many=True).data
            return Response({"result" : "success", "data": reviews_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class AddPatientsHospitals(APIView):
    permission_classes = [IsAuthenticatedHospital]

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
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def post(request):
        try:
            data = request.data
            DoctorsManagement.add_hospital_admin(request, data)
            return Response({"result" : "success", "message": "New Department Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchAllReviews(APIView):
    permission_classes = [IsAuthenticatedHospital]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            all_reviews = DoctorsManagement.get_all_reviews(request, data)
            reviews_serialized_data = DoctorReviewsWithPatientsAndDoctorSerializer(all_reviews, many=True).data

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
            return Response({"result" : "success", "message": "Hospital added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)
