from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    courses_enrolled = models.PositiveIntegerField(default=0, help_text="Number of courses the user is currently learning")
    courses_completed = models.PositiveIntegerField(default=0, help_text="Number of courses fully finished")
    total_learning_hours = models.FloatField(default=0.0, help_text="Total hours spent watching videos")
    average_quiz_score = models.FloatField(default=0.0, help_text="Percentage average on quizzes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
