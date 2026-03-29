from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Media', {
            'fields': ('video_url',)
        }),
    )
