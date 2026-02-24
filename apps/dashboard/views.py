from django.shortcuts import redirect, render
from django.views.generic import View

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html', {
        
    })
    
class RedirectHomeView(View):
    
    def get(self, request, *args, **kwargs):
        
        user = request.user
        
        if getattr(user, 'is_instructor', False):
            return redirect('instructor:course_list')
        else:
            return redirect('student:course_list')