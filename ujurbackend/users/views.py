from django.db.models import Q, F
from rest_framework.views import APIView
from rest_framework.response import Response

from patients.models import Patient
from patients.serializer import PatientSerializer
from users.manager import UserManager
import jwt



class PhoneOtp(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            UserManager.phone_otp_send(data)
            return Response({"result" : "success"}, 200)
        except Exception as err:
            return Response(str(err), 500)


class PhoneOtpVerify(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            user_exist = UserManager.phone_otp_verify(data)
            token = False
            if user_exist == "user exists":
                email = data.get('email', False)
                if len(email) == 10:
                    try:
                        int_email = int(email)
                        email = "+91-" + str(email)
                    except ValueError:
                        pass
                filters = Q()
                filters &= Q(user__email=email) | Q(ujur_id=email) | Q(user__phone=email)
                filters &= Q(created_by=None) | Q(created_by=F('id'))
                patient = Patient.objects.get(filters)
                patient_data = PatientSerializer(patient).data
                payload = {
                    'patient': patient.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')

                return Response({"result" : "success", "userType":user_exist, "token":token, "patient":patient_data}, 200)
            else:
                return Response({"result" : "failure", "message":"Invalid  Mobile No/UJUR ID or Password"}, 200)
        except Exception as err:
            return Response(str(err), 500)

class  PhoneSignUpVerify(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            verification_code = UserManager.phone_sign_up_otp(data)
            return Response({"result" : "success", "verification_code":verification_code['data']['verificationId']}, 200)

        except Exception as err:
            return Response(str(err), 500)

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            verification_verify = UserManager.phone_signup_verify(data)
            return Response({"result" : "success", "data":verification_verify}, 200)

        except Exception as err:
            return Response(str(err), 500)
