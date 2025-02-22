# yourapp/consumers.py
import json
import os

import requests
from channels.generic.websocket import AsyncWebsocketConsumer

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")


class VoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Expecting JSON with a "message" key containing transcribed text.
        data = json.loads(text_data)
        user_text = data.get("message", "")

        # Call the Eleven Labs API (this is synchronous; for production consider an async client)
        api_url = "https://api.elevenlabs.io/v1/conversation/synthesize"
        payload = {
            "text": user_text,
            "voice_id": "YOUR_DESIRED_VOICE_ID",  # Replace with your desired voice ID
        }
        headers = {
            "Authorization": f"Bearer {ELEVEN_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            data_resp = response.json()
            audio_url = data_resp.get("audio_url")  # Adjust based on API response
            # Send back the audio URL and original text
            await self.send(
                json.dumps({"audio_url": audio_url, "user_text": user_text})
            )
        else:
            # Send an error message back to the client
            await self.send(json.dumps({"error": response.text}))
