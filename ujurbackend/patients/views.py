from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from doctors.manager import DoctorsManagement
from doctors.serializer import DoctorReviewsWithPatientsAndDoctorSerializer, \
    HospitalReviewsWithPatientsAndDoctorSerializer, AppointmentWithDoctorSerializer
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

class changeJwt(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            patientId = request.data.get("patientId")
            token = request.headers.get("jwtToken")
            decoded_token = jwt.decode(token, "secretKeyRight34", algorithms=['HS256'])

            if token and patientId:
                payload = {
                    'phone_number': decoded_token.get("phone_number"),
                    'patient': patientId
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
            personal_patient, all_linked_patient = PatientManager.get_patient_profile(request, data)
            personal_data = PatientDetailsSerializer(personal_patient).data
            all_linked_patient_data = PatientDetailsSerializer(all_linked_patient, many=True).data
            return Response({"result" : "success", "data": personal_data, "linked_patient": all_linked_patient_data}, 200)
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

class changeProfileValue(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            user_change = PatientManager.change_profile_user(request, data)
            return Response({"result" : "success", "message": "Profile Changed Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class fetchCustomerReviews(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            user_change = PatientManager.fetch_customer_reviews(request, data)
            personal_data = DoctorReviewsWithPatientsAndDoctorSerializer(user_change, many=True).data
            return Response({"result" : "success", "message": "Profile Changed Successfully", "data":personal_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class fetchCustomerReviewsHospital(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            user_change = PatientManager.fetch_customer_hospital_reviews(request, data)
            personal_data = HospitalReviewsWithPatientsAndDoctorSerializer(user_change, many=True).data
            return Response({"result" : "success", "message": "Profile Changed Successfully", "data":personal_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)

class fetchLabReports(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            user_change = PatientManager.fetch_lab_reports_customers(request, data)
            personal_data = AppointmentWithDoctorSerializer(user_change, many=True).data
            return Response({"result" : "success", "message": "Profile Changed Successfully", "data":personal_data}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)


class uploadCustomerLabReport(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            data = request.data
            user_change = PatientManager.upload_customer_lab_report(request, data)
            return Response({"result" : "success", "message": "Lab Report Uploaded Successfully"}, 200)
        except Exception as e:
            return Response({"result" : "failure", "message":str(e)}, 500)
