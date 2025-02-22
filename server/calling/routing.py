# yourapp/routing.py
from django.urls import re_path

from .consumers import VoiceChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/voice-chat/$", VoiceChatConsumer.as_asgi()),
]
