from django.urls import path
from ..views import student

app_name = "student"

urlpatterns = [
    path('courses/',
        student.CourseListView.as_view(), name="course_list"),
    path('detail/<str:slug>', 
        student.CourseDetailView.as_view(), name="course_detail"),
    path('<str:slug>/lessons/', student.course_lessons, name="course_lessons")
]
