from django.urls import path
from app_room.api.v1.views.room_views import chat_room

urlpatterns = [
    path('', chat_room, name='chat_room'),
]
