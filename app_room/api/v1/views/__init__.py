"""
Views package 

Structure:
- room_views: views for room management
- message_views: views for message management
- room_management_views: views for room management
"""

# Template Views (HTML Pages)
from .room_views import (
    ChatRoomView,
    RoomListPageView
)

# API Views - Messages
from .message_views import (
    MessageHistoryView,
    ImageUploadView
)

# API Views - Room Management
from .room_management_views import (
    RoomListView,
    RoomDetailView,
    RoomCreateView,
    RoomJoinView,
    RoomLeaveView
)


__all__ = [
    # Template Views
    'ChatRoomView',
    'RoomListPageView',
    
    # API Views - Messages
    'MessageHistoryView',
    'ImageUploadView',
    
    # API Views - Room Management
    'RoomListView',
    'RoomDetailView',
    'RoomCreateView',
    'RoomJoinView',
    'RoomLeaveView',
]
