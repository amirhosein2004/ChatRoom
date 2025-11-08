from django.urls import path, include


app_name = 'room_api_v1'


urlpatterns = [
    # Template/Page routes (this should be first to catch /rooms/list/ before /rooms/)
    path("", include("app_room.api.v1.urls.room")),

    # API routes (messages, rooms management)
    path("", include("app_room.api.v1.urls.messages")),
    path("", include("app_room.api.v1.urls.room_management")),
]
