from typing import Dict, Any
from .models import Course

class CourseService:
    """
    Encapsulates all business logic for the Course model.
    Keeps Fat Models / Fat Views away by decoupling logic into services.
    """
    
    @staticmethod
    def create_course(validated_data: Dict[str, Any]) -> Course:
        # Additional business logic (like notifications, slug generation, etc.) goes here
        course = Course.objects.create(**validated_data)
        return course

    @staticmethod
    def update_course(course: Course, validated_data: Dict[str, Any]) -> Course:
        # Additional business logic (like checks before updating) goes here
        for attr, value in validated_data.items():
            setattr(course, attr, value)
        course.save()
        return course

    @staticmethod
    def delete_course(course: Course) -> None:
        # Additional business logic (like deleting related S3 assets) goes here
        course.delete()
