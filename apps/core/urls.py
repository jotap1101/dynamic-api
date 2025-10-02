from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.core.views import DynamicModelViewSet

# Create router for dynamic viewset
router = DefaultRouter()
router.register(r"", DynamicModelViewSet, basename="dynamic")

urlpatterns = [
    # Dynamic API endpoints
    path("", include(router.urls)),
]
