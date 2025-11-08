"""
Views for HTML (Template Views)

These views display HTML pages and fetch data from API.
"""
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app_room.models.room import Room


class ChatRoomView(APIView):
    """
    Show Chat Room Page
    
    - Message data is loaded from API (/api/room/v1/messages/)
    - Realtime connection is established via WebSocket
    
    URLs:
    - GET /api/room/v1/ - Public Chat (public_chat)
    - GET /api/room/v1/{slug}/ - Chat of a specific room
    """
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chat/room.html'
    
    def get(self, request, slug=None):
        """
        Show Chat Room Page
        
        Args:
            slug: Room slug (optional - if not provided, public_chat is displayed)
        """
        if slug:
            # Specific room
            room = get_object_or_404(Room, slug=slug)
            room_name = room.name
            room_slug = room.slug
        else:
            # Public room
            room_name = 'Public Chat'
            room_slug = 'public_chat'
        
        return Response({
            'room_name': room_name,
            'room_slug': room_slug,
        })


class RoomListPageView(APIView):
    """
    Show Room List Page
    
    - Room data is loaded from API (/api/room/v1/rooms/)
    - Create new room using API
    
    URL: GET /api/room/v1/rooms/list/
    """
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chat/room_list.html'
    
    def get(self, request):
        """
        Show Room List Page
        """
        return Response({})
