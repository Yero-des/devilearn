from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import User

TIMEZONE_CHOICES = [
    ("UTC-6", "UTC-6 Ciudad de México"),
    ("UTC-5", "UTC-5 Lima"),
    ("UTC-3", "UTC-3 Buenos aires")
]

class ProfileForm(forms.ModelForm):
    
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Nombres")
    last_name = forms.CharField(label="Apellidos")
    
    class Meta:
        model = Profile
        fields = ['photo', 'company', 'profession', 'timezone']
        widgets = {
            'timezone': forms.Select(choices=TIMEZONE_CHOICES),
            'photo': forms.FileInput(attrs={
                'id': "fileUpload",
                'style': "display:none;",
                'form': "profileForm"
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            
    def save(self, commit=True):
        # Traemos las asignaciones del mismo metodo
        profile = super().save(commit=False)
        user = self.instance.user
        
        if user:        
            user.email = self.cleaned_data.get('email')
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
        
        if commit:
            user.save()
            profile.save()
            
        return profile
    
class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombres')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    email = forms.EmailField(required=True, label='Correo electrónico')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya esta registrado")
        
        return email
    