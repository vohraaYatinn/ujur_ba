from admin.models import mainAdminDetails

class AdminManagement:
    @staticmethod
    def login_main_admin(data):
        email = data.get("email")
        password = data.get("password")
        check_admin = mainAdminDetails.objects.filter(email=email, password=password)
        if check_admin.exists():
            return check_admin[0]
        return False