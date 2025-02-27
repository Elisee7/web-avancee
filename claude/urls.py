# ecep_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App URLs
    path('api/', include('api.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/content/', include('content.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/licenses/', include('licenses.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/sync/', include('sync.urls')),
    #path('api/dashboard/', include('dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)