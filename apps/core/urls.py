from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import DynamicModelViewSet

# Create router for dynamic viewset
router = DefaultRouter()
router.register(
    r"(?P<database>[^/.]+)/(?P<model>[^/.]+)", DynamicModelViewSet, basename="dynamic"
)

urlpatterns = [
    # JWT authentication endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Dynamic API endpoints
    path("", include(router.urls)),
]
