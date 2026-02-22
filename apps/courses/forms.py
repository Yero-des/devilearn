from django import forms
from .models import Text, File, Image, Video
from django.core.files.uploadedfile import UploadedFile

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
            
            if file.size > 2 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede superar los 2 MB')
                        
        return file
     
            
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file and isinstance(file, UploadedFile):
            
            if file.size > 2 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede superar los 2 MB')
            
            if file.content_type not in [
                'image/jpeg',
                'image/png',
                'image/gif'
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
            
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede superar los 2 MB')
                        
        return file