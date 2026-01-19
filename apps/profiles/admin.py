from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, InstructorProfile
from apps.courses.admin import Enrollment

# Register your models here.

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1

class InstructorProfileInline(admin.StackedInline):
    model = InstructorProfile
    can_delete = False
    verbose_name = 'Perfil de instructor'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [InstructorProfileInline, EnrollmentInline]
    list_display = BaseUserAdmin.list_display + ('is_instructor',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rol personalizado', {
            'fields': ('is_instructor',)
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('is_instructor',)
        }),
    )    

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio',)
    search_fields = ('user__username', 'user__first_name',)