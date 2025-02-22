import json

from agents.chat import ChatAgent
from agents.match import MatchAgent
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from type.user_info import UserInfo


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Store conversation history

        self.chat_agent = ChatAgent(
            user_info=UserInfo(
                first_name="Daniel", age=38, gender="Male", location="New York"
            )
        )

        self.match_agent = MatchAgent()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            user_message = text_data_json["message"]

            # Add user message to conversation history
            response = self.chat_agent.chat(user_message)

            # Send response back to WebSocket
            await self.send(text_data=json.dumps({"message": response}))

        except Exception as e:
            # Send error message back to WebSocket
            await self.send(
                text_data=json.dumps(
                    {"message": f"Sorry, I encountered an error: {str(e)}"}
                )
            )


class VoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
