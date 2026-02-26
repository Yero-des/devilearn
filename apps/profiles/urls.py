from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileUpdateView.as_view(), name='profile'),  
    path('settings/password/', views.CustomPasswordChangeView.as_view(), name='change_password')  
]
