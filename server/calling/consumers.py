# yourapp/consumers.py
import asyncio
import base64
import json

import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation

from .websocket_audio_interface import WebSocketAudioInterface


class VoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "voice_chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        try:
            # Create audio interface with websocket
            audio_interface = WebSocketAudioInterface(self)

            # Initialize ElevenLabs conversation
            self.conversation = Conversation(
                client=ElevenLabs(api_key=settings.ELEVENLABS_API_KEY),
                agent_id="GExUCktNNwJ82r2Nrlbs",
                requires_auth=True,
                audio_interface=audio_interface,  # Use our custom interface
                callback_agent_response=self.handle_agent_response,
                callback_user_transcript=self.handle_user_transcript,
            )
            # Start the conversation session
            self.conversation.start_session()
        except Exception as e:
            print(f"Error initializing ElevenLabs conversation: {str(e)}")
            await self.close()

    def handle_agent_response(self, response):
        print(f"Agent response: {response}")

    def handle_user_transcript(self, transcript):
        print(f"User transcript: {transcript}")

    async def disconnect(self, close_code):
        # Clean up ElevenLabs connection
        if hasattr(self, "conversation"):
            self.conversation.end_session()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Pass the audio data to our audio interface
            print(f"Received audio data: {bytes_data}")
        else:
            # Handle text messages if needed
            data = json.loads(text_data)
            message = data.get("message", "")
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "broadcast_text", "message": message}
            )

    async def broadcast_audio(self, event):
        audio = event["audio"]
        await self.send(bytes_data=audio)

    async def broadcast_text(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
