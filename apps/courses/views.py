from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from .services import CourseService

class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Courses.
    Delegates creation, updates, and deletion to the CourseService.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        # Override default to use our service layer
        serializer.instance = CourseService.create_course(serializer.validated_data)

    def perform_update(self, serializer):
        # Override default to use our service layer
        serializer.instance = CourseService.update_course(
            course=serializer.instance, 
            validated_data=serializer.validated_data
        )

    def perform_destroy(self, instance):
        # Override default to use our service layer
        CourseService.delete_course(instance)
