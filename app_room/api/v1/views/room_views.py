from django.shortcuts import render
from app_room.models.room import Message

def chat_room(request):
    messages = Message.objects.all()[:50]
    return render(request, 'chat/room.html', {'messages': messages})