import jwt
from rest_framework.permissions import IsAuthenticated, IsDoctorAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from admin.manager import AdminManagement
from doctors.manager import DoctorsManagement


class MainAdminLogin(APIView):
    permission_classes = []

    @staticmethod
    def get(request):
        try:
            data = request.query_params
            login_admin = AdminManagement.login_main_admin(request)
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

