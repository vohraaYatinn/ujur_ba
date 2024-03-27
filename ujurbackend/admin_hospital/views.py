import jwt
from rest_framework.permissions import IsAuthenticated, IsDoctorAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from admin_hospital.manager import AdminMainManagement
from admin_hospital.serializer import AppointmentSerializer, AppointmentWithDepartmentandDoctorSerializer
from doctors.manager import DoctorsManagement
from hospitals.manager import HospitalManager
from hospitals.serializer import HospitalSerializer, HospitalSerializerWithDoctors


class MainAdminLogin(APIView):
    permission_classes = []

    @staticmethod
    def post(request):
        try:
            data = request.data
            login_admin = AdminMainManagement.login_main_admin(data)
            if login_admin:
                payload = {
                    'email': login_admin.email,
                    'admin': login_admin.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
                return Response({"result": "success", "message": "Admin login successfully", "token": token}, 200)
            else:
                return Response({"result": "failure", "message": "Please Check the Username or Password", "token": False}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

class FetchAllHospital(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_data = HospitalManager.fetch_all_admin_hospital(data)
            hospital_serialized_data = HospitalSerializer(hospital_data, many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchHospitalDetails(APIView):
    @staticmethod
    def get(request):
        try:
            hospital_doc_data = HospitalManager.fetch_all_doctors_hospital()
            hospital_serialized_data = HospitalSerializerWithDoctors(hospital_doc_data).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchAllAppointmentsAdmin(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_data = DoctorsManagement.fetch_all_appointments(data)
            appointment_data = AppointmentWithDepartmentandDoctorSerializer(hospital_data, many=True).data
            return Response({"result": "success", "data": appointment_data}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

