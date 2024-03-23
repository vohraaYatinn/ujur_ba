import random
from common_constants import CommonConstants
from users.models import otpPhone, UsersDetails


class UserManager:
    @staticmethod
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
        phone_number = data.get('phoneNumber', False)
        first_digit = data.get("firstDigit", False)
        second_digit = data.get("secondDigit", False)
        third_digit = data.get("thirdDigit", False)
        fourth_digit = data.get("fourthDigit", False)
        fifth_digit = data.get("fifthDigit", False)
        otp = first_digit+second_digit+third_digit+fourth_digit+fifth_digit
        if phone_number and otp:
            try:
                otpPhone.objects.get(phone_number=phone_number, otp=otp)
            except otpPhone.DoesNotExist:
                raise Exception("Otp Entered is Invalid or Expired, Please Try again")
            check_if_user_exist = UsersDetails.objects.filter(phone=phone_number)
            if check_if_user_exist:
                response = "user exists"
            else:
                UsersDetails.objects.create(phone=phone_number, role=CommonConstants.user_roles['patient'])
                response = "new user"
            return response
        else:
            raise Exception("Phone and Otp is required")
