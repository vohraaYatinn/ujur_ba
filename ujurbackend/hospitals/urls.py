from django.urls import include, path

from hospitals.views import HospitalFetchDashboard, HospitalFetchDoco, FetchLabReports, HospitalAdminLogin, \
    HospitalDoctors, HospitalDoctorsProfile, HospitalAddDoctors, HandlePasswordRequest, FetchDoctorLeaveRequests, \
    FetchHospitalDepartments, FetchHospitalReviews, FetchPatientsHospitals, AddPatientsHospitals

urlpatterns = [
    path(r'dashboard-hospitals/', HospitalFetchDashboard.as_view(), name="dashboard-hospitals"),
    path(r'dashboard-hospitals/', HospitalFetchDashboard.as_view(), name="phone_otp"),
    path(r'doctors-hospitals/', HospitalFetchDoco.as_view(), name="doctors-hospitals"),
    path(r'fetch_patients_lab_reports/', FetchLabReports.as_view(), name="fetch-lab-reports"),

    # hospital dashboards
    path(r'login-hospital-admin/', HospitalAdminLogin.as_view(), name="login-hospital-admin"),
    path(r'hospital-doctors/', HospitalDoctors.as_view(), name="hospital-doctors"),
    path(r'doctor-profile-hospital/', HospitalDoctorsProfile.as_view(), name="doctor-profile-hospital"),
    path(r'add-doctor-hospital/', HospitalAddDoctors.as_view(), name="doctor-add-hospital"),
    path(r'reset-password-requests/', HandlePasswordRequest.as_view(), name="reset-password-requests"),
    path(r'change-doctors-passwword/', HandlePasswordRequest.as_view(), name="change-doctors-password"),
    path(r'fetch-leave-requests/', FetchDoctorLeaveRequests.as_view(), name="fetch-leave-requests"),
    path(r'perform-leave-action/', FetchDoctorLeaveRequests.as_view(), name="perform-leave-action"),
    path(r'fetch-appointments-for-hospitals/', FetchDoctorLeaveRequests.as_view(), name="fetch-appointments-for-hospitals"),
    path(r'fetch-departments-for-hospitals/', FetchHospitalDepartments.as_view(), name="fetch-departments-for-hospitals"),
    path(r'fetch-reviews-for-hospitals/', FetchHospitalReviews.as_view(), name="fetch-reviews-for-hospitals"),
    path(r'fetch-patients-for-hospitals/', FetchPatientsHospitals.as_view(), name="fetch-patients-for-hospitals"),
    path(r'add-patients-for-hospitals/', AddPatientsHospitals.as_view(), name="add-patients-for-hospitals"),

]