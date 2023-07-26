from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path(r"api/", include("api.urls")),
    path(r"admin/", admin.site.urls),
]
