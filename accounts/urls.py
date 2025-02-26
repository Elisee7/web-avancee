# accounts/urls.py

from django.urls import path
from .views import UserRegistrationView, UserProfileView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
]