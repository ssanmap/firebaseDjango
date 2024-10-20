from django.contrib import admin
from django.urls import path, include
from .views import verify_token
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verify-token/', verify_token, name='verify_token'),
    path('api/', include(router.urls)),
]
