from django.urls import include, path
from patients.views import patientSignup, BookAppointmentPatient, FetchPatientAppointments, fetchPatientPersonalDetails, \
    addNewProfilePatient, changeJwt, changeProfileValue

urlpatterns = [
    path(r'patient-signup/', patientSignup.as_view(), name="phone_otp"),
    path(r'change_jwt_patient/', changeJwt.as_view(), name="phone_otp"),
    path(r'book_appointment-patient/', BookAppointmentPatient.as_view(), name="book-appointment"),
    path(r'fetch-appointments/', FetchPatientAppointments.as_view(), name="fetch-patients-appointment"),
    path(r'fetch-personal-info-patients/', fetchPatientPersonalDetails.as_view(), name="fetch-patients-personal-details"),
    path(r'add-new-profile/', addNewProfilePatient.as_view(), name="add-new-profile"),
    path(r'change-profile-values/', changeProfileValue.as_view(), name="change-profile-values"),
]
