from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return render(request, "profiles/profile.html", {
        
    })

class ProfileDetailView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profiles/profile.html'    
    fields = ['email', 'photo', 'first_name', 'last_name',
              'company', 'professional_title', 'time_zone']
    context_object_name = 'user'
    
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={
            'pk': self.object.id
        })