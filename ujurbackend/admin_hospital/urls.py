from django.urls import path

from admin_hospital.views import MainAdminLogin, FetchAllHospital, FetchHospitalDetails, FetchAllAppointmentsAdmin, \
    FetchAllDoctors, HandleAdmin, HandleDeleteAdmin, HandleHospitalAdmin, FetchMainDashboardDashboard, \
    FetchHospitalDashboardDashboard, DeleteHospitalAdminByUjur, DeletePatientAdminByUjur, CancelAppointmentAdminByUjur, \
    EditHospitalDetails, addAdminDoctors, editAdminDoctors, EditHospitalAdminPassword, EditCustomerAdminPassword, \
    AddPromoCode, deletePromoCode, fetchAllReviewsHospital, completedDoctorGraph
from hospitals.views import FetchAllDepartments, AddDepartmentsAdmin, fetchAllReviews, FetchPatientsAdmin, \
    AddHospitalAdmin

urlpatterns = [
    # doctor app api
    path(r'fetch-dashboard-details-admin/', FetchMainDashboardDashboard.as_view(), name="fetch-dashboard-details-admin"),
    path(r'fetch-dashboard-details-hospital/', FetchHospitalDashboardDashboard.as_view(), name="fetch-dashboard-details-hospital"),
    path(r'login-main-admin/', MainAdminLogin.as_view(), name="login-main-admin"),
    path(r'all-hospitals/', FetchAllHospital.as_view(), name="all-hospitals"),
    path(r'hospital-profile/', FetchHospitalDetails.as_view(), name="all-hospitals"),
    path(r'edit-hospital-profile/', EditHospitalDetails.as_view(), name="all-hospitals"),
    path(r'fetch-all-admin-doctors/', FetchAllDoctors.as_view(), name="all-hospitals"),
    path(r'add-admin-doctors/', addAdminDoctors.as_view(), name="all-hospitals"),
    path(r'edit-admin-doctors/', editAdminDoctors.as_view(), name="all-hospitals"),
    path(r'fetch-appointments-for-all-admin/', FetchAllAppointmentsAdmin.as_view(), name="fetch-appointments-for-all-admin"),
    path(r'fetch-all-department-or-hospitals/', FetchAllDepartments.as_view(), name="fetch-all-department-or-hospitals"),
    path(r'add-department-admin/', AddDepartmentsAdmin.as_view(), name="add-department-admin"),
    path(r'fetch-all-reviews/', fetchAllReviews.as_view(), name="fetch-all-reviews"),
    path(r'fetch-patients-admin/', FetchPatientsAdmin.as_view(), name="fetch-patients-admin"),
    path(r'add-hospital-admin/', AddHospitalAdmin.as_view(), name="add-hospital-admin"),
    path(r'add-admin/', HandleAdmin.as_view(), name="add-hospital-admin"),
    path(r'get-admins-data/', HandleAdmin.as_view(), name="add-hospital-admin"),
    path(r'delete-handle/', HandleDeleteAdmin.as_view(), name="add-hospital-admin"),
    path(r'fetch-hospital-admin/', HandleHospitalAdmin.as_view(), name="fetch-hospital-admin"),
    path(r'add-hospital-admin-user/', HandleHospitalAdmin.as_view(), name="add-hospital-admin"),
    path(r'delete-hospital-admin-by-ujur/', DeleteHospitalAdminByUjur.as_view(), name="delete-hospital-admin-by-ujur"),
    path(r'delete-patient-admin-by-ujur/', DeletePatientAdminByUjur.as_view(), name="delete-patient-admin-by-ujur"),
    path(r'cancel-appointment-admin-by-ujur/', CancelAppointmentAdminByUjur.as_view(), name="cancel-appointment-admin-by-ujur"),
    path(r'edit-hospital-admin-password/', EditHospitalAdminPassword.as_view(), name="forgot-password-request"),
    path(r'edit-customer-password/', EditCustomerAdminPassword.as_view(), name="edit-customer-password"),
    path(r'view-promo-code/', AddPromoCode.as_view(), name="add-promo-code"),
    path(r'add-promo-code/', AddPromoCode.as_view(), name="add-promo-code"),
    path(r'delete-promo-code/', deletePromoCode.as_view(), name="delete-promo-code"),
    path(r'fetch-all-reviews-hospitals/', fetchAllReviewsHospital.as_view(), name="fetch-all-reviews-hospitals"),
    path(r'completed-doctor-graph/', completedDoctorGraph.as_view(), name="completed-doctor-graph"),

]

