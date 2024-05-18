from django.urls import include, path

from hospitals.views import HospitalFetchDashboard, HospitalFetchDoco, FetchLabReports, HospitalAdminLogin, \
    HospitalDoctors, HospitalDoctorsProfile, HospitalAddDoctors, HandlePasswordRequest, FetchDoctorLeaveRequests, \
    FetchHospitalDepartments, FetchHospitalReviews, FetchPatientsHospitals, AddPatientsHospitals, \
    FetchHospitalAppointments, GetSoftwareDepartments, AddDepartmentsHospitals, HandleDeleteHospital, HandleDoctors, \
    HandleDepartments, HospitalDoctorReviews, HandleHospitalAdmins, handleHospitalMedicines, handleReferToMedicines, \
    cancelAppointments, HospitalEditDoctors, uploadLabReport, hospitalAnalyticsGraphs, genderGraphFetch, ageGraphsFetch

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
    path(r'edit-doctor-profile/', HospitalEditDoctors.as_view(), name="edit-doctor-profile"),
    path(r'reset-password-requests/', HandlePasswordRequest.as_view(), name="reset-password-requests"),
    path(r'change-doctors-passwword/', HandlePasswordRequest.as_view(), name="change-doctors-password"),
    path(r'fetch-leave-requests/', FetchDoctorLeaveRequests.as_view(), name="fetch-leave-requests"),
    path(r'perform-leave-action/', FetchDoctorLeaveRequests.as_view(), name="perform-leave-action"),
    path(r'fetch-appointments-for-hospitals/', FetchHospitalAppointments.as_view(), name="fetch-appointments-for-hospitals"),
    path(r'fetch-departments-for-hospitals/', FetchHospitalDepartments.as_view(), name="fetch-departments-for-hospitals"),
    path(r'fetch-reviews-for-hospitals/', FetchHospitalReviews.as_view(), name="fetch-reviews-for-hospitals"),
    path(r'fetch-patients-for-hospitals/', FetchPatientsHospitals.as_view(), name="fetch-patients-for-hospitals"),
    path(r'add-patients-for-hospitals/', AddPatientsHospitals.as_view(), name="add-patients-for-hospitals"),
    path(r'fetch-software-department/', GetSoftwareDepartments.as_view(), name="fetch-software-department"),
    path(r'add-department-hospital/', AddDepartmentsHospitals.as_view(), name="add-department-hospital"),
    path(r'delete_handle/', HandleDeleteHospital.as_view(), name="delete_handle"),
    path(r'all-doctors/', HandleDoctors.as_view(), name="all-doctors"),
    path(r'all-departments/', HandleDepartments.as_view(), name="all-departments"),
    path(r'all-doctors-hospital-reviews/', HospitalDoctorReviews.as_view(), name="all-doctors-hospital-reviews"),
    path(r'fetch-hospital-admin/', HandleHospitalAdmins.as_view(), name="fetch-hospital-admin"),
    path(r'add-hospital-admin-user/', HandleHospitalAdmins.as_view(), name="add-hospital-admin-user"),
    path(r'handle-medicines-hospital/', handleHospitalMedicines.as_view(), name="handle-medicines-hospital"),
    path(r'add-medicines-hospital/', handleHospitalMedicines.as_view(), name="add-medicines-hospital"),
    path(r'handle-hospital-refer-to/', handleReferToMedicines.as_view(), name="handle-hospital-refer-to"),
    path(r'add-hospital-refer-to/', handleReferToMedicines.as_view(), name="add-hospital-refer-to"),
    path(r'cancel-given-appointment/', cancelAppointments.as_view(), name="cancel-given-appointment"),
    path(r'delete-hospital-admin/', cancelAppointments.as_view(), name="cancel-given-appointment"),
    path(r'upload-lab-reports/', uploadLabReport.as_view(), name="cancel-given-appointment"),
    path(r'hospital-analytics-graphs/', hospitalAnalyticsGraphs.as_view(), name="hospital-analytics-graphs"),
    path(r'gender-graphs-fetch/', genderGraphFetch.as_view(), name="gender-graphs-fetch"),
    path(r'age-graphs-fetch/', ageGraphsFetch.as_view(), name="age-graphs-fetch"),
]