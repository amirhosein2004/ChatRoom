from rest_framework import serializers
from app_room.models.room import Message, Room
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ['id', 'username']


class RoomSerializer(serializers.ModelSerializer):
    """Room serializer"""
    creator = UserSerializer(read_only=True)
    member_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Room
        fields = ['id', 'name', 'slug', 'description', 'creator', 'member_count',
                  'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class RoomCreateSerializer(serializers.ModelSerializer):
    """Room create serializer"""
    class Meta:
        model = Room
        fields = ['name', 'description', 'is_public']
    
    def create(self, validated_data):
        user = self.context['request'].user
        room = Room.objects.create(
            creator=user,
            **validated_data
        )
        # creator is added as the first member
        room.members.add(user)
        return room


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer"""
    user = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'content', 'image_url', 'message_type', 'timestamp']
        read_only_fields = ['id', 'room', 'user', 'content', 'image_url', 'message_type', 'timestamp']
    
    def get_image_url(self, obj):
        """Recive Image URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ImageUploadSerializer(serializers.ModelSerializer):
    """
    serializer for image upload HTTP
    
    Why use HTTP?
    - WebSocket is not suitable for sending large files
    - HTTP multipart/form-data is the best way to upload files
    - After upload, the data is sent to all users through WebSocket
    """
    username = serializers.CharField(write_only=True)
    room_slug = serializers.CharField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'username', 'room_slug', 'image', 'image_url', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def get_image_url(self, obj):
        """Recive Image URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def validate_image(self, value):
        """Validate Image"""
        # Check file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f"حجم فایل نباید بیشتر از {max_size // (1024*1024)} مگابایت باشد."
            )
        
        # Check file format
        allowed_formats = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if value.content_type not in allowed_formats:
            raise serializers.ValidationError(
                "فقط فرمت های JPEG، PNG، GIF و WebP مجاز هستند."
            )
        
        return value
    
    def create(self, validated_data):
        """Create Image Message"""
        username = validated_data.pop('username')
        room_slug = validated_data.pop('room_slug', None)
        user, created = User.objects.get_or_create(username=username)
        
        room = None
        if room_slug:
            try:
                room = Room.objects.get(slug=room_slug)
            except Room.DoesNotExist:
                pass
        
        return Message.objects.create(
            user=user,
            room=room,
            image=validated_data['image'],
            message_type='image'
        )
