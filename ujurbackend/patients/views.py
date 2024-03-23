from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from doctors.manager import DoctorsManagement
from patients.manager import PatientManager
from rest_framework.response import Response
import jwt
from patients.serializer import AppointmentSerializer, PatientDetailsSerializer


class patientSignup(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            user_exist = PatientManager.patient_signup(request, data)
            if user_exist:
                phone_number = data.get('phoneNumber', False)
                payload = {
                    'phone_number': phone_number,
                    'patient': user_exist.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')
            return Response({"result" : "success", "message": "Your profile has been made successfully", "token":token}, 200)
        except Exception as e:
            return Response({"result": "failure", "message": str(e)}, 500)


class BookAppointmentPatient(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.query_params
            DoctorsManagement.book_appointment(data)
            return Response({"result" : "success", "message": "Your Appointment has been booked successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class FetchPatientAppointments(APIView):
    @staticmethod
    def get(request):
        try:
            data = request.query_params
            book_appointment = DoctorsManagement.fetch_appointments(data)
            appointment_data = AppointmentSerializer(book_appointment).data
            return Response({"result" : "success", "data": appointment_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchPatientPersonalDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            personal_patient = PatientManager.get_patient_profile(request, data)
            personal_data = PatientDetailsSerializer(personal_patient).data
            return Response({"result" : "success", "data": personal_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class addNewProfilePatient(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            user_exist = PatientManager.add_new_patient(request, data)
            return Response({"result" : "success", "message": "New User Added Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)
