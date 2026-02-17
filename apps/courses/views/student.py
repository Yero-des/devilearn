from django.shortcuts import render
from django.http import HttpResponse
from ..models import Course, Enrollment, CompletedContent, Content, Progress
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

# Course
class CourseListView(ListView):
    model = Course
    template_name = 'courses/courses.html'
    paginate_by = 8
    context_object_name = 'courses'
    
    def get_queryset(self):
        
        courses = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query: 
            courses = courses.filter(
                Q(title__icontains=query) |
                Q(owner__first_name__icontains=query)
            )
            
        return courses
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query_params: list = self.request.GET.copy()
        query = self.request.GET.get('q')
    
        if "page" in query_params:
            query_params.pop("page")
        
        query_string = query_params.urlencode()   
        
        context["query"] = query
        context["query_string"] = query_string
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        
        modules = self.object.modules.prefetch_related('contents').order_by('order')        
        total_contents = sum(module.contents.count() for module in modules )
        
        context["modules"] = modules
        # context["contents"] = contents
        context["total_contents"] = total_contents
        return context
    
    

# def course_detail(request, slug):
#     course = get_object_or_404(Course, slug=slug)
#     modules = course.modules.prefetch_related('contents').order_by('order')
#     total_contents = sum(module.contents.count() for module in modules )
#     return render(request, 'courses/course_detail.html', {
#         'course': course,
#         'modules': modules,
#         'total_contents': total_contents
#     })

def course_lessons(request, slug, content_id=None):
    course = get_object_or_404(Course, slug=slug)
    course_title = course.title
    course_slug = course.slug
    modules = course.modules.prefetch_related('contents').order_by('order')
    
    # Enrollment
    Enrollment.objects.get_or_create(user=request.user, course=course)
    
    # get all contents
    all_contents = [c for m in modules for c in m.contents.all()]
    total_contents = len(all_contents)
    
    completed = CompletedContent.objects.filter(
        user=request.user, 
        content__in=all_contents).values_list('content_id', flat=True)
    
    # progress by module
    for module in modules:
        module.completed_count = module.contents.filter(id__in=completed).count()
        module.total_count = module.contents.count()
        
    current_content = None
    if content_id:
        current_content = get_object_or_404(Content, id=content_id, module__course=course)
        
    progress = (len(completed) / total_contents * 100) if total_contents else 0
    
    Progress.objects.update_or_create(
        user=request.user,
        course=course,
        defaults={
            'progress': progress
        }
    )
    
    return render(request, 'courses/course_lessons.html', {
        'course_title': course_title,
        'course_slug': course_slug,
        'modules': modules,
        'course': course,
        'completed_ids': set(completed),
        'current_content': current_content,
        'progress': int(progress)
    })