from django.urls import path
from users.views import PhoneOtp, PhoneOtpVerify

# from users.views import
urlpatterns = [
    path(r'phone-otp/', PhoneOtp.as_view(), name="phone_otp"),
    path(r'phone-otp-verify/', PhoneOtpVerify.as_view(), name="phone_otp_verify"),

]

