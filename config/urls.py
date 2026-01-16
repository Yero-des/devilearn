from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('apps.courses.urls'), name='courses'),
    path('dashboard/', include('apps.dashboard.urls'), name='dashboard'),
    path("profile/", include('apps.profiles.urls'), name="profiles")
]
