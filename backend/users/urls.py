from django.urls import path
from .views import (
    RegisterView,
    GoogleLogin,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token_refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
]
