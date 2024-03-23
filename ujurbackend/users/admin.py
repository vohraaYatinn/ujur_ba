from django.contrib import admin

from users.models import UsersDetails, otpPhone

# Register your models here.
admin.site.register(UsersDetails)
admin.site.register(otpPhone)