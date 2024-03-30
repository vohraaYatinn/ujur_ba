from django.urls import path

from admin_hospital.views import MainAdminLogin, FetchAllHospital, FetchHospitalDetails, FetchAllAppointmentsAdmin, \
    FetchAllDoctors
from hospitals.views import FetchAllDepartments, AddDepartmentsAdmin, fetchAllReviews, FetchPatientsAdmin, \
    AddHospitalAdmin

urlpatterns = [
    # doctor app api
    path(r'login-main-admin/', MainAdminLogin.as_view(), name="login-main-admin"),
    path(r'all-hospitals/', FetchAllHospital.as_view(), name="all-hospitals"),
    path(r'hospital-profile/', FetchHospitalDetails.as_view(), name="all-hospitals"),
    path(r'fetch-all-admin-doctors/', FetchAllDoctors.as_view(), name="all-hospitals"),
    path(r'fetch-appointments-for-all-admin/', FetchAllAppointmentsAdmin.as_view(), name="fetch-appointments-for-all-admin"),
    path(r'fetch-all-department-or-hospitals/', FetchAllDepartments.as_view(), name="fetch-all-department-or-hospitals"),
    path(r'add-department-admin/', AddDepartmentsAdmin.as_view(), name="add-department-admin"),
    path(r'fetch-all-reviews/', fetchAllReviews.as_view(), name="fetch-all-reviews"),
    path(r'fetch-patients-admin/', FetchPatientsAdmin.as_view(), name="fetch-patients-admin"),
    path(r'add-hospital-admin/', AddHospitalAdmin.as_view(), name="add-hospital-admin"),

]

