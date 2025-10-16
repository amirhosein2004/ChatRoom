from django.urls import re_path
from app_room.api.v1.consumers.chat_consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
]
