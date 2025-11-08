"""
URL routes for API endpoints
This file includes API routes (not HTML pages)
"""
from django.urls import path
from app_room.api.v1.views import (
    RoomListView,
    RoomCreateView,
    RoomDetailView,
    RoomJoinView,
    RoomLeaveView
)


urlpatterns = [
    # Room Management APIs
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<slug:slug>/', RoomDetailView.as_view(), name='room_detail'),
    path('rooms/<slug:slug>/join/', RoomJoinView.as_view(), name='room_join'),
    path('rooms/<slug:slug>/leave/', RoomLeaveView.as_view(), name='room_leave'),
]
