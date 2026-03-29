from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'avatar_url', 
            'courses_enrolled', 'courses_completed', 
            'total_learning_hours', 'average_quiz_score', 
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'courses_enrolled', 'courses_completed', 
            'total_learning_hours', 'average_quiz_score', 
            'created_at', 'updated_at'
        ]
