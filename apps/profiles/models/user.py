from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images', blank=True)
    company = models.CharField(max_length=50, blank=True)
    professional_title = models.CharField(max_length=100, blank=True)
    time_zone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.get_full_name() or self.username    