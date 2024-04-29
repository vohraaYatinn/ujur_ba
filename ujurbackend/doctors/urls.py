from django.urls import path
from doctors.views import DoctorFetchDashboard, DoctorFetchSingle, DoctorSlots, FavDoctor, fetchBookAppointment, \
    FetchBookingPrice, bookingConfirmationAppointment, fetchLatestAppointment, fetchAppointmentDetails, DoctorReviews, \
    fetchAppointmentDetailsPatient, doctorLogin, doctorFetchAppointments, FetchPatientsOfDoctor, fetchDoctorReviews, \
    fetchDoctorOwnProfile, doctorChangePassword, dashboardDetails, dashboardPatientsDetails, dashboarDoctorReviews, \
    changeDoctorProfile, fetchPatientProfile, fetchPatientDocument, doctorLeaveApply, patientSearching, \
    ApplyForgotPasswordRequest, handleDoctorImages, handleDoctorTokenOnRefersh, handleDoctorMedicines, writeReview

urlpatterns = [
    path(r'dashboard-doctor/', DoctorFetchDashboard.as_view(), name="dashboard-doctors"),
    path(r'get-single-doctor/', DoctorFetchSingle.as_view(), name="dashboard-doctors"),
    path(r'get-doctor-slots/', DoctorSlots.as_view(), name="doctor-slots"),
    path(r'fav-doctor/', FavDoctor.as_view(), name="fav-doctor"),
    path(r'doctor-reviews/', DoctorReviews.as_view(), name="fav-doctor"),
    path(r'doctor-reviews-create/', DoctorReviews.as_view(), name="fav-doctor"),
    path(r'fetch-price-of-booking/', fetchBookAppointment.as_view(), name="fetch-book-appointment"),
    path(r'fetch-price-of-booking-final-page/', FetchBookingPrice.as_view(), name="fetch-book-price-final"),
    path(r'confirm-booking-patient/', bookingConfirmationAppointment.as_view(), name="confirm-booking-patient"),
    path(r'fetch_latest_appointment/', fetchLatestAppointment.as_view(), name="fetch-patients-personal-details"),
    path(r'fetch_appointment_details/', fetchAppointmentDetails.as_view(), name="fetch-patients-personal-details"),
    path(r'fetch_appointments_patients/', fetchAppointmentDetailsPatient.as_view(), name="fetch-patients-details"),
    path(r'search-details/', patientSearching.as_view(), name="fetch-patients-details"),


    # doctor app api
    path(r'login-doctor/', doctorLogin.as_view(), name="login-doctor"),
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
    path(r'handle-doctor-iamges/', handleDoctorImages.as_view(), name="handle-doctor-iamges"),
    path(r'get-data-from-token/', handleDoctorTokenOnRefersh.as_view(), name="get-data-from-token"),
    path(r'handle-medicines-doctor/', handleDoctorMedicines.as_view(), name="handle-medicines-doctor"),
    path(r'add-medicines-doctor/', handleDoctorMedicines.as_view(), name="add-medicines-doctor"),
    path(r'add-reviews/', writeReview.as_view(), name="write-reviews"),
    path(r'fetch-reviews/', writeReview.as_view(), name="write-reviews"),


]

