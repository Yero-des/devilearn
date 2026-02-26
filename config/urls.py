from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from apps.dashboard.views import RedirectHomeView
from apps.profiles.views import RegisterView

urlpatterns = [
    path('', RedirectHomeView.as_view()),
    path('admin/', admin.site.urls),
    path('dashboard/', include('apps.dashboard.urls')),
    path("profile/", include('apps.profiles.urls')),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('instructor/', include('apps.courses.urls.instructor')),
    path('student/', include('apps.courses.urls.student')),
]

if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)