from django.urls import path

from admin.views import MainAdminLogin
from doctors.views import DoctorFetchDashboard, DoctorFetchSingle, DoctorSlots, FavDoctor, fetchBookAppointment, \
    FetchBookingPrice, bookingConfirmationAppointment, fetchLatestAppointment, fetchAppointmentDetails, DoctorReviews, \
    fetchAppointmentDetailsPatient, doctorLogin, doctorFetchAppointments, FetchPatientsOfDoctor, fetchDoctorReviews, \
    fetchDoctorOwnProfile, doctorChangePassword, dashboardDetails, dashboardPatientsDetails, dashboarDoctorReviews, \
    changeDoctorProfile, fetchPatientProfile, fetchPatientDocument, doctorLeaveApply, patientSearching, \
    ApplyForgotPasswordRequest, EditHospitalAdminPassword

urlpatterns = [
    # doctor app api
    path(r'login-main-admin/', MainAdminLogin.as_view(), name="login-main-admin"),
    path(r'dashboard-details/', dashboardDetails.as_view(), name="dashboard-details"),
    path(r'dashboard-patients-details/', dashboardPatientsDetails.as_view(), name="dashboard-patients-details"),
    path(r'dashboard-doctor-reviews/', dashboarDoctorReviews.as_view(), name="dashboard-doctor-reviews"),
    path(r'doctor-fetch-self-appointments/', doctorFetchAppointments.as_view(), name="doctor-fetch-self-appointments"),
    path(r'fetch-all-doctor-patients/', FetchPatientsOfDoctor.as_view(), name="fetch-all-doctor-patients"),
    path(r'fetch-my-doctor-reviews/', fetchDoctorReviews.as_view(), name="fetch-my-doctor-reviews"),
    path(r'doctor-profile/', fetchDoctorOwnProfile.as_view(), name="doctor-profile"),
    path(r'doctor-change-password/', doctorChangePassword.as_view(), name="doctor-change-password"),
    path(r'doctor-change-profile/', changeDoctorProfile.as_view(), name="doctor-change-profile"),
    path(r'fetch-patient-profile-doctor/', fetchPatientProfile.as_view(), name="fetch-patients-profile"),
    path(r'upload_document_prescription/', fetchPatientDocument.as_view(), name="upload_document_prescription"),
    path(r'doctor-fetch-leave/', doctorLeaveApply.as_view(), name="doctor-fetch-leave"),
    path(r'doctor-apply-leave/', doctorLeaveApply.as_view(), name="doctor-apply-leave-apply"),
    path(r'forgot-password-request/', ApplyForgotPasswordRequest.as_view(), name="forgot-password-request"),
    path(r'edit-hospital-admin-password/', EditHospitalAdminPassword.as_view(), name="forgot-password-request"),




]

