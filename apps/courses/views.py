from django.shortcuts import render
from django.http import HttpResponse
from .models.course import Course
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

# Create your views here.
def course_list(request):
    courses = Course.objects.all()
    query = request.GET.get('q')
    
    if query: 
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(owner__first_name__icontains=query)
        )
        
    paginator = Paginator(courses, 8)
    page_number = request.GET.get('page')
    courses_obj = paginator.get_page(page_number)
    
    query_params: list = request.GET.copy()
    
    if "page" in query_params:
        query_params.pop("page")
    
    query_string = query_params.urlencode()    
     
    return render(request, "courses/courses.html", {
        'query': query,
        'courses': courses_obj,
        'query_string': query_string
    })

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.prefetch_related('contents')
    total_contents = sum(module.contents.count() for module in modules )
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'total_contents': total_contents
    })

def course_lessons(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_title = course.title
    modules = course.modules.prefetch_related('contents')
    return render(request, 'courses/course_lessons.html', {
        'course_title': course_title,
        'modules': modules
    })