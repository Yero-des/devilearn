from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.courses.models import Course
from apps.profiles.models import Profile

# Create your views here.
class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html' 
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        courses = Course.objects.filter(enrollment__user=self.request.user).order_by('?')[:3]
        profile = Profile.objects.get(user=self.request.user)
        
        context.update({
            'courses': courses,
            'profile': profile
        })
        return context
   
class RedirectHomeView(View):
    
    def get(self, request, *args, **kwargs):
        
        user = request.user
        
        if getattr(user, 'is_instructor', False):
            return redirect('instructor:course_list')
        else:
            return redirect('student:course_list')