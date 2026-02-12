from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile
from django.contrib.auth.models import Group

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_instructor_profile(sender, instance, created, **kwargs):
    if created and instance.is_instructor:
        InstructorProfile.objects.create(user=instance)
        
        # Agregar al grupo "Instructores" si existe
        try:
            group = Group.objects.get(name="Instructores")
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass  # si no existe, no hace nada