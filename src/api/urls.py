from django.urls import include, path

urlpatterns = [
    path(r"polls/", include("api.polls.urls")),
]
