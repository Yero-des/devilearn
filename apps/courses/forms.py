from django import forms
from .models import Text, File, Image, Video, Review
from django.core.files.uploadedfile import UploadedFile

LIMIT_TYPES = {
    'kb': 1024,
    'mb': 1024 * 1024,
    'gb': 1024 * 1024 * 1024,
}

STAR_CHOICES = [(i, str(i)) for i in range(1,6)]

def validation_limit_file_size(file, limit_size, limit_type):
        
    if LIMIT_TYPES.get(limit_type):
        if file.size > limit_size * LIMIT_TYPES.get(limit_type):
            raise forms.ValidationError(f'El archivo no puede superar los {limit_size} {limit_type.upper()}')
                        

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['title', 'content']
        
        
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file and isinstance(file, UploadedFile):
            validation_limit_file_size(file, 2, 'mb')                  
         
        return file
     
            
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file and isinstance(file, UploadedFile):
            validation_limit_file_size(file, 2, 'mb')
            
            if file.content_type not in [
                'image/jpeg',
                'image/png',
                'image/gif',
            ]:
                raise forms.ValidationError(
                    "El archivo solo acepta imágenes .jpeg, .png o .gif"
                ) 
                
        return file
    
    
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file and isinstance(file, UploadedFile):
            validation_limit_file_size(file, 7, 'mb')
        
        return file
    
    
class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, 
                                widget=forms.RadioSelect(choices=STAR_CHOICES),
                                label="Calificación")
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'placeholder': "Cuentanos tu experiencia",
    }), required=False, label="Comentario")
    
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating and rating <= 5:
            raise forms.ValidationError('La calificación debe estar entre 1 y 5.')
        return rating
