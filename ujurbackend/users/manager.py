import random

from django.db import transaction
from django.db.models import Q
import requests
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

    @staticmethod
    def phone_sign_up_otp(data):
        phone = data.get('phone', False)
        forgot = data.get('forgot', False)
        if len(phone) != 10:
            raise Exception("Please enter a valid phone number")
        check_if_user_exist = UsersDetails.objects.filter(phone="+91-"+phone)
        if check_if_user_exist and not forgot:
            raise Exception("This Number is already registered")
        if forgot and not check_if_user_exist:
            raise Exception("This Number is not linked with any of your account")

        url = 'https://cpaas.messagecentral.com/verification/v3/send'
        headers = {
            'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLURFQkUyQjY4OTM4NTRBRCIsImlhdCI6MTcyMjMyNDU4MCwiZXhwIjoxODgwMDA0NTgwfQ.ihHWg1LXsk1WCjmYiCb0fA6sYrbqUORZjsw-0kr90w662ZlW7UCbb_O5GWx9_7gnzWdTA3zoGgmc1p2tQ2B4mg'
        }
        params = {
            'countryCode': '91',
            'customerId': 'C-DEBE2B6893854AD',
            'flowType': 'SMS',
            'mobileNumber': phone
        }
        response = requests.post(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Please wait 60 seconds before trying again.")
        return response.json()

    @staticmethod
    def phone_signup_verify(data):
        phone = data.get('phoneNumber', False)
        verfication_code = data.get('verificationCode', False)
        firstDigit = data.get('firstDigit', False)
        secondDigit = data.get('secondDigit', False)
        thirdDigit = data.get('thirdDigit', False)
        fourthDigit = data.get('fourthDigit', False)
        otp = str(firstDigit) + str(secondDigit) + str(thirdDigit) + str(fourthDigit)
        url = 'https://cpaas.messagecentral.com/verification/v3/validateOtp'
        headers = {
            'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLUZBNTY5QzEzODY0QjQ5OSIsImlhdCI6MTcyMDY3NzcwOSwiZXhwIjoxODc4MzU3NzA5fQ.IKzKR57hg8vdCQux-GnGbuxw1H9BMXxrrJOS_OwUl2TZ2XxDZpDof9wcvenw6yG2Ygjcpfr8dEMVizPZaWf-KA'
        }
        params = {
            'countryCode': '91',
            'mobileNumber': phone,
            'verificationId': verfication_code,
            'customerId': 'C-DEBE2B6893854AD',
            'code': otp
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("The OTP is either invalid or has expired.")

        return response.json()['data']['verificationStatus'] == 'VERIFICATION_COMPLETED'
