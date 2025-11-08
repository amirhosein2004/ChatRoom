from django.contrib import admin
from .models.room import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'creator', 'is_public', 'member_count', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'member_count']
    filter_horizontal = ['members']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp', 'room']
    search_fields = ['content', 'user__username']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        if obj.message_type == 'image':
            return '[Image]'
        return obj.content[:50] if obj.content else ''
    content_preview.short_description = 'Content'
