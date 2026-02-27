from django.shortcuts import render
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profile
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import ProfileForm, CustomRegisterForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profiles/profile.html'    
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    context_object_name = 'profile'
    
    def get_object(self, queryset = None):        
        return self.request.user.profile
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs    
    
    def form_valid(self, form):
        messages.success(self.request, "Tu perfil se ha actualizado correctamente.")
        return super().form_valid(form)
    
    
class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'settings/change_password.html'
    success_url = reverse_lazy('change_password')
    success_message = "Contraseña actualizada correctamente"
    
    
class RegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('student:course_list')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)        
        return redirect(self.success_url)
    
class CustomLoginView(LoginView):
    
    def get_success_url(self):
        user = self.request.user
        
        if user.is_instructor:
            return reverse_lazy('instructor:course_list')    
        return reverse_lazy('student:course_list')
        