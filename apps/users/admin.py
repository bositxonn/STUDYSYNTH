from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'courses_enrolled', 'courses_completed', 'total_learning_hours', 'average_quiz_score')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)
    readonly_fields = ('courses_enrolled', 'courses_completed', 'total_learning_hours', 'average_quiz_score')
    
    fieldsets = (
        ('User Context', {
            'fields': ('user', 'avatar_url')
        }),
        ('Statistics', {
            'fields': ('courses_enrolled', 'courses_completed', 'total_learning_hours', 'average_quiz_score')
        }),
    )
