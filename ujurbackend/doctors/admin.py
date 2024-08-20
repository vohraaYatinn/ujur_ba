from django.contrib import admin
from doctors.models import doctorDetails, doctorSlots, Appointment, FavDoctors, PatientDoctorReviews, DoctorLeave, \
    ResetPasswordRequest, Revenue, getChiefQuery, labTests

admin.site.register(doctorDetails)
admin.site.register(doctorSlots)
admin.site.register(Appointment)
admin.site.register(FavDoctors)
admin.site.register(PatientDoctorReviews)
admin.site.register(DoctorLeave)
admin.site.register(ResetPasswordRequest)
admin.site.register(getChiefQuery)
admin.site.register(labTests)
admin.site.register(Revenue)
