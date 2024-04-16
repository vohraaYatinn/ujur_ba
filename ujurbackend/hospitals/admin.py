from django.contrib import admin
from hospitals.models import HospitalDetails, DepartmentHospitalMapping, Department, HospitalAdmin, MedicinesName, LabReports, ReferToDoctors

admin.site.register(HospitalDetails)
admin.site.register(HospitalAdmin)
admin.site.register(Department)
admin.site.register(DepartmentHospitalMapping)
admin.site.register(LabReports)
admin.site.register(MedicinesName)
admin.site.register(ReferToDoctors)