from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..models import Course, Module
from django.urls import reverse, reverse_lazy

class InstructorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_instructor


# Course views    
    
class CourseListView(InstructorRequiredMixin, ListView):
    model = Course
    template_name = "instructor/course_list.html"
    context_object_name = "courses"
    paginate_by = 8
    
    def get_queryset(self):    
        return super().get_queryset().filter(owner=self.request.user)
    
    
class CourseCreateView(InstructorRequiredMixin, CreateView):
    model = Course
    template_name = "instructor/course_form.html"
    fields = ['title', 'slug', 'overview', 'image',
              'level', 'duration', 'category']
    success_url = reverse_lazy('instructor:course_list')
    
    def form_valid(self, form):    
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    
class CourseUpdateView(InstructorRequiredMixin, UpdateView):
    model = Course
    template_name = "instructor/course_form.html"
    fields = ['title', 'slug', 'overview', 'image',
              'level', 'duration', 'category']
    success_url = reverse_lazy('instructor:course_list')
    slug_field = "slug"
    slug_url_kwarg = "slug"
    
    def get_queryset(self):        
        return super().get_queryset().filter(owner=self.request.user)
    

class CourseDeleteView(InstructorRequiredMixin, DeleteView):
    model = Course
    template_name = "instructor/course_confirm_delete.html"
    success_url = reverse_lazy('instructor:course_list')
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "course"
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
    
    
# Module views 
class ModuleListView(InstructorRequiredMixin, ListView):
    model = Module
    template_name = "instructor/module_list.html"
    context_object_name = "modules"
    
    def get_queryset(self):
        self.course = get_object_or_404(
            Course, slug=self.kwargs['slug'], owner=self.request.user)
        return self.course.modules.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context
    