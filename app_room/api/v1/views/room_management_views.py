"""
API Views for Room Management

🔗 Routes:
- GET /api/room/v1/rooms/ - List of public rooms
- GET /api/room/v1/rooms/{slug}/ - Room details
- POST /api/room/v1/rooms/create/ - Create new room
- POST /api/room/v1/rooms/{slug}/join/ - Join room
- POST /api/room/v1/rooms/{slug}/leave/ - Leave room
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from app_room.models.room import Room
from app_room.api.v1.serializers import RoomSerializer, RoomCreateSerializer


class RoomListView(ListAPIView):
    """
    List of public rooms
    
    GET /api/room/v1/rooms/
    """
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # only public rooms
        return Room.objects.filter(is_public=True).select_related('creator')


class RoomDetailView(RetrieveAPIView):
    """
    Room details
    
    GET /api/room/v1/rooms/{slug}/
    """
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    queryset = Room.objects.all()


class RoomCreateView(APIView):
    """
    Create new room
    
    POST /api/room/v1/rooms/create/
    Body:
        - name: string (required)
        - description: string (optional)
        - is_public: boolean (default: true)
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # if user is not authenticated, create a temporary user
        if not request.user.is_authenticated:
            from django.contrib.auth.models import User
            username = request.data.get('username', 'guest')
            user, created = User.objects.get_or_create(username=username)
            request.user = user
        
        serializer = RoomCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            room = serializer.save()
            return Response(
                RoomSerializer(room, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomJoinView(APIView):
    """
    Join room
    
    POST /api/room/v1/rooms/{slug}/join/
    Body:
        - username: string (required)
    """
    permission_classes = [AllowAny]
    
    def post(self, request, slug):
        room = get_object_or_404(Room, slug=slug)
        username = request.data.get('username')
        
        if not username:
            return Response(
                {'error': 'نام کاربری الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username=username)
        
        # add user to room
        room.members.add(user)
        
        return Response(
            RoomSerializer(room, context={'request': request}).data,
            status=status.HTTP_200_OK
        )


class RoomLeaveView(APIView):
    """
    Leave room
    
    POST /api/room/v1/rooms/{slug}/leave/
    Body:
        - username: string (required)
    """
    permission_classes = [AllowAny]
    
    def post(self, request, slug):
        room = get_object_or_404(Room, slug=slug)
        username = request.data.get('username')
        
        if not username:
            return Response(
                {'error': 'نام کاربری الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=username)
            room.members.remove(user)
            return Response(
                {'message': 'با موفقیت از اتاق خارج شدید'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'کاربر یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
