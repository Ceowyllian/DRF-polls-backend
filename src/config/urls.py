from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(r"api/", include("api.urls")),
    path(r"admin/", admin.site.urls),
    path(r"oas3/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        r"oas3/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        r"oas3/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
