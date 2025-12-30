from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"), # /courses
    path("detail/", views.course_detail, name="course_detail"),
    path("lessons/", views.course_lessons, name="course_lessons")
]
