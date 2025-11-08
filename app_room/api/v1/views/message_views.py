from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404

from app_room.models.room import Message, Room
from app_room.api.v1.serializers import (
    MessageSerializer, 
    ImageUploadSerializer
)


class MessageHistoryView(APIView):
    """
    Get Message List - Only for initial load
    
    - limit is constant: 50 last messages
    - can be filtered by room_slug
    
    GET /api/room/v1/messages/
    GET /api/room/v1/messages/?room_slug=general
    """
    permission_classes = [AllowAny]
    
    def get(self, request, slug=None):
        offset = int(request.query_params.get('offset', 0))
        
        if slug and slug != 'public_chat':
            room = get_object_or_404(Room, slug=slug)
            messages = room.messages.select_related('user').order_by('-timestamp')[offset:offset+50]
        else:
            messages = Message.objects.filter(room__isnull=True).select_related('user').order_by('-timestamp')[offset:offset+50]
        
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)


class ImageUploadView(APIView):
    """
    Upload Image HTTP
    
    Why HTTP?
    - WebSocket is not suitable for sending large files
    - HTTP with multipart/form-data is the best way to upload files
    - After upload, the data is sent to all users through WebSocket
    
    POST /api/room/v1/upload-image/
    Body (multipart/form-data):
        - image: file
        - username: string
        - room_slug: string (optional)
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            message = serializer.save()
            
            # define group name based on room
            room_name = message.room.slug if message.room else 'public_chat'
            
            # send notification to WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{room_name}',
                {
                    'type': 'chat_message',
                    'message_id': message.id,
                    'username': message.user.username,
                    'message': '',
                    'image_url': request.build_absolute_uri(message.image.url),
                    'message_type': 'image',
                    'timestamp': message.timestamp.isoformat()
                }
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
