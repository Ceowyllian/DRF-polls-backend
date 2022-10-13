from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('custom_auth.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
