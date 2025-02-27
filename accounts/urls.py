# accounts/urls.py

from django.urls import path
from django.contrib import admin
from accounts.views import register, profile, login_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#from .views import UserRegistrationView, UserProfileView, CustomTokenObtainPairView

#urlpatterns = [
#    path('register/', UserRegistrationView.as_view(), name='user-register'),
#    path('profile/', UserProfileView.as_view(), name='user-profile'),
#    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
#]

urlpatterns = [
    path('register/', register, name='user-register'),
    path('profile/', profile, name='user-profile'),
    path('login/', login_view, name='token-obtain-pair'),
]