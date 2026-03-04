from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.IndexTemplateView.as_view(), name="dashboard")
]
