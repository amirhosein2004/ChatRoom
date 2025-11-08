"""
URL routes for HTML pages (Template Views)
this file includes HTML page routes
"""
from django.urls import path
from app_room.api.v1.views import ChatRoomView, RoomListPageView


urlpatterns = [
    # room list page
    path('rooms/list/', RoomListPageView.as_view(), name='room_list_page'),
    
    # public chat room
    path('chat/', ChatRoomView.as_view(), name='chat_room'),
    
    # specific chat room
    path('chat/<slug:slug>/', ChatRoomView.as_view(), name='chat_room_detail'),
]
