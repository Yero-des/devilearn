from django.urls import path
from ..views import instructor

app_name = "instructor"

urlpatterns = [
    # Courses URLs
    path('courses/', 
         instructor.CourseListView.as_view(), name='course_list'),
    path('course/create/', 
         instructor.CourseCreateView.as_view(), name="course_create"),
    path('course/<str:slug>/edit/',
        instructor.CourseUpdateView.as_view(), name="course_edit"), 
    path('course/<str:slug>/delete/', 
        instructor.CourseDeleteView.as_view(), name="course_delete"),
    # Modules URLs    
    path('course/<str:slug>/modules/', 
        instructor.ModuleListView.as_view(), name="module_list"),
    path('course/<str:slug>/modules/create', 
        instructor.ModuleCreateView.as_view(), name="module_create"),
    path('modules/<int:pk>/edit', 
        instructor.ModuleUpdateView.as_view(), name="module_edit"),
    path('module/<int:pk>/delete/',
        instructor.ModuleDeleteView.as_view(), name="module_delete"),
    # Content URLs
    path('module/<int:module_id>/contents',
        instructor.ContentListView.as_view(), name="content_list"),
    
]
