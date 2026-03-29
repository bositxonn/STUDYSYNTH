from django.contrib import admin
from .models import Field, Category, Course, Lesson, Quiz, Question

admin.site.register(Field)
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'category', 'legacy_category')
        }),
        ('Media', {
            'fields': ('video_url',)
        }),
    )
