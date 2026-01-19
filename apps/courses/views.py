from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def course_list(request):
    courses = [
        {
            'id': 1,
            'level': 'Principiante',
            'rating': 4.8,
            'course_title': "Python: Fundamentos hasta los detalles",
            'instructor': "Alison Walsh",
            'course_image': "images/curso_1.jpg",
            'instructor_image': "https://randomuser.me/api/portraits/women/68.jpg"
        },
        {
            'id': 2,
            'level': 'Intermedio',
            'rating': 5.0,
            'course_title': "Guia para principiantes sobre gestión empresarial exitosa: Negocios y más",
            'instructor': "Patty Kutch",
            'course_image': "images/curso_2.jpg",
            'instructor_image': "https://randomuser.me/api/portraits/women/20.jpg"
        },
        {
            'id': 3,
            'level': 'Principiante',
            'rating': 5.0,
            'course_title': "Una fascinante teoría de la probabilidad. Practica. Aplicación. Como superar ...",
            'instructor': "Alonso Murray",
            'course_image': "images/curso_3.jpg",
            'instructor_image': "https://randomuser.me/api/portraits/men/32.jpg"
        },
        {
            'id': 4,
            'level': 'Principiante',
            'rating': 5.0,
            'course_title': "Introducción: Aprendizaje Automático y LLM. Implementación en Software Moderno.",
            'instructor': "Gregory Harris",
            'course_image': "images/curso_4.jpg",
            'instructor_image': "https://randomuser.me/api/portraits/men/45.jpg"
        },
    ]
    
    return render(request, "courses/courses.html", {
        'courses': courses
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