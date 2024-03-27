from django.urls import path

from admin_hospital.views import MainAdminLogin, FetchAllHospital, FetchHospitalDetails, FetchAllAppointmentsAdmin
from doctors.views import DoctorFetchDashboard, DoctorFetchSingle, DoctorSlots, FavDoctor, fetchBookAppointment, \
    FetchBookingPrice, bookingConfirmationAppointment, fetchLatestAppointment, fetchAppointmentDetails, DoctorReviews, \
    fetchAppointmentDetailsPatient, doctorLogin, doctorFetchAppointments, FetchPatientsOfDoctor, fetchDoctorReviews, \
    fetchDoctorOwnProfile, doctorChangePassword, dashboardDetails, dashboardPatientsDetails, dashboarDoctorReviews, \
    changeDoctorProfile, fetchPatientProfile, fetchPatientDocument, doctorLeaveApply, patientSearching, \
    ApplyForgotPasswordRequest
from hospitals.views import FetchAllDepartments, AddDepartmentsAdmin

urlpatterns = [
    # doctor app api
    path(r'login-main-admin/', MainAdminLogin.as_view(), name="login-main-admin"),
    path(r'all-hospitals/', FetchAllHospital.as_view(), name="all-hospitals"),
    path(r'hospital-profile/', FetchHospitalDetails.as_view(), name="all-hospitals"),
    path(r'fetch-all-hospital-doctors/', FetchAllHospital.as_view(), name="all-hospitals"),
    path(r'fetch-appointments-for-all-admin/', FetchAllAppointmentsAdmin.as_view(), name="fetch-appointments-for-all-admin"),
    path(r'fetch-all-department-or-hospitals/', FetchAllDepartments.as_view(), name="fetch-all-department-or-hospitals"),
    path(r'add-department-admin/', AddDepartmentsAdmin.as_view(), name="add-department-admin"),


]

