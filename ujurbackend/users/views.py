from rest_framework.views import APIView
from rest_framework.response import Response

from patients.models import Patient
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
                phone_number = data.get('phoneNumber', False)
                patient = Patient.objects.get(user__phone = phone_number)
                payload = {
                    'phone_number': phone_number,
                    'patient': patient.id
                }
                token = jwt.encode(payload, 'secretKeyRight34', algorithm='HS256')

            return Response({"result" : "success", "userType":user_exist, "token":token}, 200)
        except Exception as err:
            return Response(str(err), 500)