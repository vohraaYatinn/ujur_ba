from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from ujurbackend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v2/users/', include('users.urls'), name="users"),
    path(r'api/v2/patients/', include('patients.urls'), name="patients"),
    path(r'api/v2/doctors/', include('doctors.urls'), name="doctors"),
    path(r'api/v2/hospitals/', include('hospitals.urls'), name="hospitals"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
