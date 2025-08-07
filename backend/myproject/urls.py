from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/', include(('users.urls', 'users'), namespace="users")),
    path('api/', include(('companies.urls', 'companies'), namespace="companies")),
    path('api/watchlist/', include(('watchlist.urls', 'watchlist'), namespace="watchlist")),

    # Swagger/OpenAPI Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

