from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def course_list(request):
    return HttpResponse("This works")

def course_detail(request):
    return HttpResponse("This works")

def course_lessons(request):
    return HttpResponse("This works")