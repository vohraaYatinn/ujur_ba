import jwt
from rest_framework.permissions import IsAuthenticated, IsDoctorAuthenticated, IsAuthenticatedAdminPanel, \
    IsAuthenticatedHospital
from rest_framework.views import APIView
from rest_framework.response import Response

from admin_hospital.manager import AdminMainManagement
from admin_hospital.serializer import AppointmentSerializer, AppointmentWithDepartmentandDoctorSerializer, \
    DoctorModelWithDepartmentHospitalSerializer, AdminsSerailizer, HospitalAdminsSerailizer, PromoCodeSerializer, \
    HospitalReviewsWithPatientsSerializer
from doctors.manager import DoctorsManagement
from doctors.serializer import DoctorReviewsWithPatientsAndDoctorHospitalSerializer, \
    DoctorReviewsWithPatientsAndDoctorSerializer
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
                    'main_admin': login_admin.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
                return Response({"result": "success", "message": "Admin login successfully", "token": token}, 200)
            else:
                return Response({"result": "failure", "message": "Please Check the Username or Password", "token": False}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class FetchMainDashboardDashboard(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def get(request):
        try:
            counts = AdminMainManagement.fetch_main_admin_dashboard()
            return Response({"result" : "success", "data": counts}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchHospitalDashboardDashboard(APIView):
    permission_classes = [IsAuthenticatedHospital]
    @staticmethod
    def get(request):
        try:
            counts = AdminMainManagement.fetch_main_hospital_dashboard(request)
            return Response({"result" : "success", "data": counts}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchAllHospital(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
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
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def get(request):
        try:
            data=request.query_params
            hospital_id = data.get('hospitalId', False)
            hospital_doc_data, review = HospitalManager.fetch_all_doctors_hospital(hospital_id)
            hospital_serialized_data = HospitalSerializerWithDoctors(hospital_doc_data).data
            review_serialized_data = DoctorReviewsWithPatientsAndDoctorSerializer(review, many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data, "reviews":review_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class EditHospitalDetails(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def post(request):
        try:
            data=request.data
            hospital_id = data.get('hospitalId', False)
            hospital_doc_data = HospitalManager.edit_admin_hospital(hospital_id, data)
            return Response({"result" : "success", "message": "hospital_serialized_data"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchAllAppointmentsAdmin(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_data = DoctorsManagement.fetch_all_appointments(data)
            appointment_data = AppointmentWithDepartmentandDoctorSerializer(hospital_data, many=True).data
            return Response({"result": "success", "data": appointment_data}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)

class FetchAllDoctors(APIView):
    @staticmethod
    def get(request):
        try:
            data=request.query_params
            hospital_id = data.get('hospitalId', False)
            hospital_doc_data = HospitalManager.fetch_all_doctors_hospital(hospital_id)
            hospital_serialized_data = HospitalSerializerWithDoctors(hospital_doc_data).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchAllDoctors(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            hospital_doc_data = HospitalManager.fetch_all_doctors_admin(data)
            hospital_serialized_data = DoctorModelWithDepartmentHospitalSerializer(hospital_doc_data,many=True).data
            return Response({"result" : "success", "data": hospital_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandleAdmin(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            admin = AdminMainManagement.fetch_admin_data(data)
            admin_serialized_data = AdminsSerailizer(admin,many=True).data
            return Response({"result" : "success", "data": admin_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)
    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = AdminMainManagement.add_admin_form(data)
            return Response({"result" : "success", "message": "UJUR Admin added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandleDeleteAdmin(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]


    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = AdminMainManagement.handle_delete_admin(data)
            return Response({"result" : "success", "message": "Admin Deleted successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class HandleHospitalAdmin(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            admin = AdminMainManagement.fetch_hospital_admin_data(data)
            admin_serialized_data = HospitalAdminsSerailizer(admin,many=True).data
            return Response({"result" : "success", "data": admin_serialized_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = AdminMainManagement.add_hospital_admin_data(data)
            return Response({"result" : "success", "message": "Hospital Admin added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)



class DeleteHospitalAdminByUjur(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = AdminMainManagement.delete_hospital_admin_by_ujur(data)
            return Response({"result" : "success", "message": "Hospital Admin Deleted Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class DeletePatientAdminByUjur(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = AdminMainManagement.delete_patient_admin_by_ujur(data)
            return Response({"result" : "success", "message": "Patient Deleted Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class CancelAppointmentAdminByUjur(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            admin = AdminMainManagement.cancel_appointment_by_ujur(data)
            return Response({"result" : "success", "message": "Appointment canceled Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)



class addAdminDoctors(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            doctor_obj = DoctorsManagement.add_new_admin_doctor_hospital(request, data)
            return Response(
                {"result": "success", "message": "New Doctor added successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class editAdminDoctors(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            doctor_obj = DoctorsManagement.edit_doctor_hospital(request, data)
            return Response(
                {"result": "success", "message": "Doctor edited successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)



class EditHospitalAdminPassword(APIView):
    permission_classes = []
    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.edit_hospital_admin_password(request, data)
            return Response(
                {"result": "success", "message": "Reset Password Request has been applied Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class EditCustomerAdminPassword(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            HospitalManager.edit_patient_admin_password(request, data)
            return Response(
                {"result": "success", "message": "Reset Password Request has been applied Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class AddPromoCode(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            AdminMainManagement.add_promo_code(request, data)
            return Response(
                {"result": "success", "message": "New Promo Code has been created"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

    @staticmethod
    def get(request):
        try:
            data = AdminMainManagement.get_promo_code(request)
            seralizer_data = PromoCodeSerializer(data,many=True).data
            return Response(
                {"result": "success", "message": "New Promo Code has been created","data":seralizer_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class deletePromoCode(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def post(request):
        try:
            data = request.data
            AdminMainManagement.delete_promo_code(request, data)
            return Response(
                {"result": "success", "message": "Selected Promo Code has been deleted"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class fetchAllReviewsHospital(APIView):
    permission_classes = [IsAuthenticatedAdminPanel]
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            reviews = HospitalManager.fetch_all_hospital_reviews(data)
            seralizer_data = HospitalReviewsWithPatientsSerializer(reviews,many=True).data
            return Response(
                {"result": "success", "data": seralizer_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)