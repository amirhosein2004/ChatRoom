from django.urls import path, include


urlpatterns = [
    path("v1/", include("app_room.api.v1.urls")),
]
