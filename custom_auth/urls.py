from .apiviews import LoginView, UserCreate

from django.urls import path


urlpatterns = [
    path('registration/', UserCreate.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]
