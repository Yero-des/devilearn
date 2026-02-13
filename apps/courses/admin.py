from django.contrib import admin
from .models import (Category, Course, CourseCategory,
                     Module, Enrollment, Progress, Review, Content,
                     Image, Text, File, Video)

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    
    
class CategoryInline(admin.TabularInline):
    '''Tabular Inline View for Category'''

    model = CourseCategory
    extra = 1
    
    
class ModuleInline(admin.TabularInline):
    '''Tabular Inline View for Module'''

    model = Module
    extra = 1
    
class ContentInline(admin.TabularInline):
    '''Tabular Inline View for Content'''

    model = Content
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline, CategoryInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'overview']


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('course', 'category')
    list_filter = ('category',)
    search_fields = ('course__title',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
    list_display = ('title', 'course')
    list_filter = ('title', 'course__title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress', 'status', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'course__title')
    fieldsets = (
        ('Relacion', {
            "fields": ('user', 'course'),
        }),
        ('Detalles', {
            "fields": ('status', 'progress'),
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'course__title', 'comment')

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('module__title', 'content_type', 'item', 'order')
    list_filter = ('module',)
    ordering = ['-module__title', 'order']
    
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'updated_at', 'content')
    ordering = ('-id',)
    
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'updated_at', 'file')
    ordering = ('-id',)
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'updated_at', 'file')
    ordering = ('-id',)
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'updated_at', 'file')
    ordering = ('-id',)