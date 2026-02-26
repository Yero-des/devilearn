from django.db import models
from .user import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    @property
    def photo_url(self):
        return self.photo.url if self.photo != "" else "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg"