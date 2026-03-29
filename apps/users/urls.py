from django.urls import path
from .views import UserProfileView

app_name = 'users'

urlpatterns = [
    path('me/profile/', UserProfileView.as_view(), name='my-profile'),
]
