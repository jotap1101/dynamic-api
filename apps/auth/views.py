from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


@extend_schema_view(
    post=extend_schema(
        summary="Obtain JWT token pair",
        description="Obtain a new JWT access and refresh token pair by providing valid user credentials.",
        tags=["Authentication"],
        request=inline_serializer(
            name="TokenObtainRequest",
            fields={
                "username": serializers.CharField(),
                "password": serializers.CharField(),
            },
        ),
        responses={
            200: inline_serializer(
                name="TokenObtainResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                },
            )
        },
    ),
)
class TokenObtainPairView(TokenObtainPairView):
    """
    View to obtain JWT token pair (access and refresh).
    """

    pass


@extend_schema_view(
    post=extend_schema(
        summary="Refresh JWT access token",
        description="Refresh the JWT access token using a valid refresh token.",
        tags=["Authentication"],
        request=inline_serializer(
            name="TokenRefreshRequest",
            fields={
                "refresh": serializers.CharField(),
            },
        ),
        responses={
            200: inline_serializer(
                name="TokenRefreshResponse",
                fields={
                    "access": serializers.CharField(),
                },
            )
        },
    ),
)
class TokenRefreshView(TokenRefreshView):
    """
    View to refresh JWT access token using a valid refresh token.
    """

    pass


@extend_schema_view(
    post=extend_schema(
        summary="Verify JWT token",
        description="Verify if a JWT token is valid and not expired.",
        tags=["Authentication"],
        request=inline_serializer(
            name="TokenVerifyRequest",
            fields={
                "token": serializers.CharField(help_text="JWT token to verify"),
            },
        ),
        responses={
            200: None,
            401: inline_serializer(
                name="TokenVerifyError",
                fields={
                    "detail": serializers.CharField(help_text="Error description"),
                    "code": serializers.CharField(help_text="Error code"),
                },
            ),
        },
    ),
)
class TokenVerifyView(TokenVerifyView):
    """
    View to verify the validity of a JWT token.
    """

    pass


@extend_schema_view(
    post=extend_schema(
        summary="Blacklist JWT refresh token",
        description="Blacklist a JWT refresh token to prevent its further use.",
        tags=["Authentication"],
        request=inline_serializer(
            name="TokenBlacklistActionRequest",
            fields={
                "refresh": serializers.CharField(
                    help_text="JWT refresh token to blacklist"
                ),
            },
        ),
        responses={
            204: None,
            401: inline_serializer(
                name="TokenBlacklistError",
                fields={
                    "detail": serializers.CharField(help_text="Error description"),
                    "code": serializers.CharField(help_text="Error code"),
                },
            ),
        },
    ),
)
class TokenBlacklistView(TokenBlacklistView):
    """
    View to blacklist a JWT refresh token.
    """

    pass
