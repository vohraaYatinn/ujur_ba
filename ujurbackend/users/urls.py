from django.urls import path
from users.views import PhoneOtp, PhoneOtpVerify, PhoneSignUpVerify

# from users.views import
urlpatterns = [
    path(r'phone-otp/', PhoneOtp.as_view(), name="phone_otp"),
    path(r'phone-otp-verify/', PhoneOtpVerify.as_view(), name="phone_otp_verify"),
    path(r'phone-signup-otp/', PhoneSignUpVerify.as_view(), name="phone-signup-otp"),
    path(r'phone-signup-otp-verify/', PhoneSignUpVerify.as_view(), name="phone-signup-otp-verify"),

]

