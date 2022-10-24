from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
