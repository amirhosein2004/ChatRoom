from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Room(models.Model):
    """Room model"""
    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    description = models.TextField(blank=True, null=True, verbose_name='description')
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, 
        related_name='created_rooms', verbose_name='creator'
    )
    members = models.ManyToManyField(
        User, related_name='joined_rooms', 
        blank=True, verbose_name='members'
    )
    is_public = models.BooleanField(default=True, verbose_name='public')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def member_count(self):
        return self.members.count()


class Message(models.Model):
    """Message model"""
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
    ]
    
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='messages', 
        null=True, blank=True, verbose_name='room'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='user'
    )
    content = models.TextField(
        blank=True, null=True, verbose_name='content'
    )
    image = models.ImageField(
        upload_to='chat_images/', blank=True, null=True, 
        verbose_name='image'
    )
    message_type = models.CharField(
        max_length=10, choices=MESSAGE_TYPE_CHOICES, 
        default='text', verbose_name='message type'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name='timestamp'
    )

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        room_name = self.room.name if self.room else 'Public'
        if self.message_type == 'image':
            return f'{self.user.username} in {room_name}: [image]'
        return f'{self.user.username} in {room_name}: {self.content[:50]}'
