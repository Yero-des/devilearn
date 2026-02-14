from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from ..models import Course, Module, Content, Text, Image, File, Video
from ..forms import TextForm, ImageForm, FileForm, VideoForm
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, reverse_lazy
from django.forms.models import modelform_factory
from django.http import HttpResponseForbidden

CONTENT_MODELS = {
    'text': {
        'model': Text,
        'form': TextForm
    },
    'video': {
        'model': Video,
        'form': VideoForm
    },
    'image': {
        'model': Image,
        'form': ImageForm
    },
    'file': {
        'model': File,
        'form': FileForm
    },
}

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
        return self.course.modules.all().order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context
    
    
class ModuleCreateView(InstructorRequiredMixin, CreateView):
    model = Module
    fields = ['title', 'description']
    template_name = 'instructor/module_form.html'
    
    def form_valid(self, form):
        course = get_object_or_404(
            Course, slug=self.kwargs['slug'], owner=self.request.user)
        form.instance.course = course
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('instructor:module_list', kwargs={
            'slug': self.object.course.slug
        })


class ModuleUpdateView(InstructorRequiredMixin, UpdateView):
    model = Module
    fields = ['title', 'description']
    template_name = 'instructor/module_form.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(course__owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('instructor:module_list', kwargs={
            'slug': self.object.course.slug
        })


class ModuleDeleteView(InstructorRequiredMixin, DeleteView):
    model = Module
    template_name = 'instructor/module_confirm_delete.html'
    context_object_name = "module"
    
    def get_queryset(self):
        return super().get_queryset().filter(course__owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('instructor:module_list', kwargs={
            'slug': self.object.course.slug # El object no se borra asi que aun se puede pasar normalmente
        })
        

# Content
class ContentListView(InstructorRequiredMixin, ListView):
    model = Content
    template_name = 'instructor/content_list.html'
    context_object_name = 'contents'
    
    def get_queryset(self):
        self.module = get_object_or_404(Module, id=self.kwargs['module_id'], course__owner=self.request.user)
        return self.module.contents.all().select_related('content_type').order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module"] = self.module
        return context
    

class ContentCreateUpdateView(InstructorRequiredMixin, View):
    template_name = 'instructor/content_form.html'
    
    def get_model(self, model_name):
        return CONTENT_MODELS.get(model_name).get('model')
    
    def get_form(self, model, form, *args, **kwargs):
        Form = modelform_factory(model, form)
        return Form(*args, **kwargs)
        
    def dispatch(self, request, module_id=None, model_name=None, id=None, *args, **kwargs):                
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        self.form = CONTENT_MODELS.get(model_name).get('form')
        self.obj = None
        
        if id:
            try:
                content = Content.objects.select_related('content_type').get(
                    object_id=id,
                    content_type=ContentType.objects.get_for_model(self.model),
                    module=self.module,                    
                )
                self.obj = content.item
            except Content.DoesNotExist:
                return HttpResponseForbidden("No tienes permiso o tipo invalido")            
        
        return super().dispatch(request, module_id=module_id, model_name=model_name, id=id, *args, **kwargs)
    
    
    def get(self, request, module_id, model_name, id=None):            
        form = self.get_form(self.model, self.form, instance=self.obj)
        return render(request, self.template_name, {
            'form': form,
            'content': self.obj
        })
        
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, self.form, instance=self.obj, 
                             data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            
            if not id:
                Content.objects.create(module=self.module, item=obj)
            
            return redirect('instructor:content_list', module_id=self.module.id)    
            
        return render(request, self.template_name, {
            'form': form,
            'content': self.obj
        })
                

class ContentDeleteview(InstructorRequiredMixin, DeleteView):
    model = Content
    template_name = 'instructor/content_confirm_delete.html'
    context_object_name = 'content'
    
    def get_queryset(self):
        return super().get_queryset().filter(module__course__owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('instructor:content_list', kwargs={
            'module_id': self.object.module.id
        })