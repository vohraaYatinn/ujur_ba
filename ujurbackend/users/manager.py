import random

from django.db import transaction
from django.db.models import Q

from common_constants import CommonConstants
from users.models import otpPhone, UsersDetails


class UserManager:
    @staticmethod
    @transaction.atomic
    def phone_otp_send(data):
        phone_number = data.get('phoneNumber', False)
        otp = random.randint(10000,99999)
        otp = 99999
        if phone_number and len(phone_number) == 10:
            otp_obj = otpPhone.objects.filter(phone_number=phone_number)
            if otp_obj:
                otp_obj.update(otp=otp)
            else:
                otpPhone.objects.create(phone_number=phone_number, otp=otp)
        else:
            raise Exception("phone number should valid")


    @staticmethod
    def phone_otp_verify(data):
        email = data.get('email', False)
        if len(email) == 10:
            try:
                int_email = int(email)
                email = "+91-" + str(email)
            except ValueError:
                pass
        password = data.get("password", False)
        filters = Q()
        filters &= Q(email=email) | Q(user_patient_table__ujur_id=email) | Q(phone=email)
        filters &= Q(password=password)
        check_if_user_exist = UsersDetails.objects.filter(filters)
        if check_if_user_exist:
            return "user exists"
        return False
