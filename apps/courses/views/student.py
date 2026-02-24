from django.shortcuts import redirect, render
from django.http import HttpResponse
from ..models import Course, Enrollment, CompletedContent, Content, Progress
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# Course
class CourseListView(LoginRequiredMixin, ListView):
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
        
        context.update({
            'query': query,
            'query_string': query_string
        }) 
        
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
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
    

class CourseLessonsView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_lessons.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        course = self.object
        modules = course.modules.prefetch_related('contents').order_by('order')
        
        # Enrollment
        Enrollment.objects.get_or_create(user=self.request.user, course=course)
        
        # get all contents
        all_contents = [c for m in modules for c in m.contents.all()]
        total_contents = len(all_contents)
        
        completed = CompletedContent.objects.filter(
            user=self.request.user, 
            content__in=all_contents).values_list('content_id', flat=True)
        
        # progress by module
        for module in modules:
            module.completed_count = module.contents.filter(id__in=completed).count()
            module.total_count = module.contents.count()
        
        # get content_id from URL parameters
        content_id = self.kwargs.get('content_id')
        current_content = None
        if content_id:
            current_content = get_object_or_404(Content, id=content_id, module__course=course)
        
        progress = (len(completed) / total_contents * 100) if total_contents else 0
        
        Progress.objects.update_or_create(
            user=self.request.user,
            course=course,
            defaults={
                'progress': progress
            }
        )
        
        previous_content = None
        next_content = None
        current_contents = None
        current_position = None
        current_total_contents = None
        
        if current_content:
            
            current_contents = Content.objects.filter(module=current_content.module)
            
            previous_content = current_contents.filter(
                order__lt=current_content.order            
            ).last()    
            
            next_content = current_contents.filter(
                order__gt=current_content.order
            ).first()    
            
            contents_list = list(current_contents)
            
            current_total_contents = len(contents_list)
            current_position = contents_list.index(current_content) + 1            
            
        context.update({
            'course_title': course.title,
            'course_slug': course.slug,
            'modules': modules,
            'completed_ids': set(completed),
            'current_content': current_content,
            'progress': int(progress),
            'previous_content': previous_content,
            'next_content': next_content,
            'current_total_contents': current_total_contents,
            'current_position': current_position,
        })
        
        return context
    

class MarkCompleteView(LoginRequiredMixin, View):
    
    def post(self, request, content_id, *args, **kwargs):
        content = get_object_or_404(Content, id=content_id)        
        CompletedContent.objects.get_or_create(user=request.user, content=content)
        
        next_content = Content.objects.filter(
            module=content.module,
            order__gt=content.order
        ).order_by('order').first()
        
        if next_content:
            return redirect('student:course_lessons', slug=content.module.course.slug, content_id=next_content.id)
        
        return redirect('student:course_lessons', slug=content.module.course.slug)
    