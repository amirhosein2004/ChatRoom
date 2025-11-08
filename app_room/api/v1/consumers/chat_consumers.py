import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from app_room.models.room import Message, Room
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket Consumer For management chat
    support text and image type messages
    """
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', 'public_chat')
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recieve message from client"""
        data = json.loads(text_data)
        message_type = data.get('message_type', 'text')
        username = data.get('username')
        
        if message_type == 'text':
            # text messages
            message = data.get('message', '')
            message_id = await self.save_text_message(username, message, self.room_name)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': message_id,
                    'message': message,
                    'username': username,
                    'message_type': 'text'
                }
            )
        
        elif message_type == 'image':
            # image messages - just notif (uploaded with HTTP)
            image_url = data.get('image_url')
            message_id = data.get('message_id')
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': message_id,
                    'message': '',
                    'username': username,
                    'message_type': 'image',
                    'image_url': image_url
                }
            )

    async def chat_message(self, event):
        """Send message to client"""
        message_type = event.get('message_type', 'text')
        response_data = {
            'message_id': event.get('message_id'),
            'username': event['username'],
            'message_type': message_type,
            'timestamp': event.get('timestamp', '')
        }
        
        if message_type == 'text':
            response_data['message'] = event['message']
        elif message_type == 'image':
            response_data['image_url'] = event.get('image_url')
            response_data['message'] = ''
        
        await self.send(text_data=json.dumps(response_data))

    @database_sync_to_async
    def save_text_message(self, username, message, room_name):
        """Save text message to database"""
        user, created = User.objects.get_or_create(username=username)
        
        # Find room (if not public_chat)
        room = None
        if room_name and room_name != 'public_chat':
            try:
                room = Room.objects.get(slug=room_name)
            except Room.DoesNotExist:
                pass
        
        msg_obj = Message.objects.create(
            user=user,
            room=room,
            content=message,
            message_type='text'
        )
        return msg_obj.id
