from django.shortcuts import render
from django.http import HttpResponse
from .models.course import Course
from django.db.models import Q
from django.core.paginator import Paginator

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
    page_number = request.GET.get("page")
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

def course_detail(request):
    course = {
        'course_title': 'Django Aplicaciones',
        'course_link': 'course_lessons',
        'course_image': 'images/curso_2.jpg',
        'info_course': {
            'lessons': 79,
            'duration': 8,
            'instructor': 'Ricardo Cúellar'
        },
        'course_content': [
            {
                'id': 1,
                'name': 'Introducción la curso',
                'lessons': [
                    {
                        'name': '¿Que aprenderas en el curso?',
                        'type': 'video'
                    },
                    {
                        'name': '¿Como usar la plataforma?',
                        'type': 'article'
                    },
                    {
                        'name': '¿Que herramientas necesito?',
                        'type': 'article'
                    },
                ]
            }
        ]
    }
    return render(request, 'courses/course_detail.html', {
        'course': course
    })

def course_lessons(request):
    lesson = {
        'course_title': 'Django Aplicaciones',
        'course_progress': 30,
        'course_content': [
            {
                'id': 1,
                'name': 'Introducción la curso',
                'total_lessons': 6,
                'complete_lessons': 3,
                'lessons': [
                    {
                        'name': '¿Que aprenderas en el curso?',
                        'type': 'video'
                    },
                    {
                        'name': '¿Como usar la plataforma?',
                        'type': 'article'
                    },
                    {
                        'name': '¿Que herramientas necesito?',
                        'type': 'article'
                    },
                ]
            },
            {
                'id': 2,
                'name': 'Django principios',
                'total_lessons': 12,
                'complete_lessons': 2,
                'lessons': [
                    {
                        'name': '¿Que aprenderas en el curso?',
                        'type': 'video'
                    },
                    {
                        'name': '¿Como usar la plataforma?',
                        'type': 'article'
                    },
                    {
                        'name': '¿Que herramientas necesito?',
                        'type': 'article'
                    },
                ]
            }
        ]
    }
    return render(request, 'courses/course_lessons.html', {
        'lesson': lesson
    })