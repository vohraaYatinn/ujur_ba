from django.urls import include, path
from patients.views import patientSignup, BookAppointmentPatient, FetchPatientAppointments, fetchPatientPersonalDetails, \
    addNewProfilePatient, changeJwt, changeProfileValue, fetchCustomerReviews, fetchCustomerReviewsHospital, \
    fetchLabReports, uploadCustomerLabReport, applyCoupon, fetchPaymentDetails, paymentVerifyCheck

urlpatterns = [
    path(r'patient-signup/', patientSignup.as_view(), name="phone_otp"),
    path(r'change_jwt_patient/', changeJwt.as_view(), name="phone_otp"),
    path(r'book_appointment-patient/', BookAppointmentPatient.as_view(), name="book-appointment"),
    path(r'fetch-appointments/', FetchPatientAppointments.as_view(), name="fetch-patients-appointment"),
    path(r'fetch-personal-info-patients/', fetchPatientPersonalDetails.as_view(), name="fetch-patients-personal-details"),
    path(r'add-new-profile/', addNewProfilePatient.as_view(), name="add-new-profile"),
    path(r'change-profile-values/', changeProfileValue.as_view(), name="change-profile-values"),
    path(r'fetch_customer_reviews/', fetchCustomerReviews.as_view(), name="fetch_customer_reviews"),
    path(r'fetch_customer_reviews_hospitals/', fetchCustomerReviewsHospital.as_view(), name="fetch_customer_reviews"),
    path(r'fetch_patients_lab_reports/', fetchLabReports.as_view(), name="fetch_customer_reviews"),
    path(r'upload_customer_lab_report/', uploadCustomerLabReport.as_view(), name="upload_customer_lab_report"),
    path(r'apply_coupons/', applyCoupon.as_view(), name="apply_coupon"),
    path(r'payment-order-fetch/', fetchPaymentDetails.as_view(), name="payment-order-fetch"),
    path(r'confirm-payment/', paymentVerifyCheck.as_view(), name="payment-verify-check"),
]
