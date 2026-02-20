from django.urls import path
from ..views import student

app_name = "student"

urlpatterns = [
    path('courses/',
        student.CourseListView.as_view(), name="course_list"),
    path('detail/<str:slug>', 
        student.CourseDetailView.as_view(), name="course_detail"),
    path('<str:slug>/lessons/', 
        student.CourseLessonsView.as_view(), name="course_lessons"),
    path('<str:slug>/lessons/<int:content_id>/', 
        student.CourseLessonsView.as_view(), name="course_lessons"),
    path('content/<int:content_id>/complete',
        student.MarkCompleteView.as_view(), name="content_mark_complete")
]
