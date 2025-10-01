"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

prefix = "api/v1/"

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),
    # JWT Authentication endpoints
    path(f"{prefix}token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path(f"{prefix}token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(f"{prefix}token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        f"{prefix}token/blacklist/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    # Dynamic API endpoints
    path(f"{prefix}", include("apps.core.urls")),
    # API schema and documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
