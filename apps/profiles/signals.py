from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile, Profile
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_instructor_profile(sender, instance, created, **kwargs):
    if created and instance.is_instructor:
        InstructorProfile.objects.create(user=instance)
        
        # Agregar al grupo "Instructores" si existe
        try:
            group = Group.objects.get(name="Instructores")
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass  # si no existe, no hace nada
        
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()