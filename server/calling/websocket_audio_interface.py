from typing import Callable

from elevenlabs.conversational_ai.conversation import AudioInterface


class WebSocketAudioInterface(AudioInterface):
    def __init__(self, websocket):
        self.websocket = websocket
        self.input_callback = None

    def start(self, input_callback: Callable[[bytes], None]):
        """Initialize the audio interface with the input callback."""
        self.input_callback = input_callback

    def stop(self):
        """Clean up resources."""
        self.input_callback = None

    def output(self, audio: bytes):
        """Send audio data through websocket."""
        # Using asyncio.create_task since we're in an async context
        import asyncio

        asyncio.create_task(self.websocket.send(bytes_data=audio))

    def interrupt(self):
        """Handle interruption of audio output."""
        # Optionally send a control message to the client to stop audio playback
        pass

    def process_incoming_audio(self, audio_data: bytes):
        """Process incoming audio data from websocket."""
        if self.input_callback:
            self.input_callback(audio_data)
