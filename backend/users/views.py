from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

User = get_user_model()

@extend_schema(
    summary="Register a new user",
    description="Registers a user using email, name, and password.",
    request=RegisterSerializer,
    responses={201: RegisterSerializer},
    tags=["Authentication"]
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

@extend_schema(
    summary="Login with email and password",
    description="Returns access and refresh JWT tokens upon successful login.",
    tags=["Authentication"]
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


@extend_schema(
    summary="Refresh JWT token",
    description="Takes a refresh token and returns a new access token.",
    tags=["Authentication"]
)
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


@extend_schema(
    summary="Login with Google",
    description="Authenticates user via Google and returns JWT tokens.",
    responses={
        200: OpenApiExample(
            "JWT Token Example",
            value={"access": "jwt-access-token", "refresh": "jwt-refresh-token"},
            response_only=True,
        )
    },
    tags=["Authentication"]
)
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        token = RefreshToken.for_user(self.user)
        return Response({
            "access": str(token.access_token),
            "refresh": str(token),
        })
