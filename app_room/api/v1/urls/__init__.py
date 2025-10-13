from django.urls import path, include


app_name = 'room_api_v1'

urlpatterns = [
    path("", include("app_room.api.v1.urls.room")),
]
