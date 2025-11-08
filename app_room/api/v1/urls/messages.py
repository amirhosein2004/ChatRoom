from django.urls import path
from app_room.api.v1.views import (
    MessageHistoryView,
    ImageUploadView,
)

urlpatterns = [
    path('messages/', MessageHistoryView.as_view(), name='message_history'),
    path('messages/<slug:slug>/', MessageHistoryView.as_view(), name='message_history_room'),
    path('upload-image/', ImageUploadView.as_view(), name='upload_image'),
]
