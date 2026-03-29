from rest_framework import views, response, permissions, status
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileView(views.APIView):
    """
    Retrieve or update the authenticated user's profile and statistics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
