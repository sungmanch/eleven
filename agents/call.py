import os
import sys
import signal
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

class CallAgent:
    def __init__(self):
        # Initialize ElevenLabs client and conversation
        api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=api_key)
        self.audio_interface = DefaultAudioInterface()
        self.conversation = Conversation(
            self.client,
            agent_id="GExUCktNNwJ82r2Nrlbs",
            requires_auth=bool(api_key),
            audio_interface=self.audio_interface,
            callback_agent_response=lambda response: print(f"Agent: {response}"),
            callback_agent_response_correction=lambda original, corrected: print(
                f"Agent: {original} -> {corrected}"
            ),
            callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
        )
        self.conversation.start_session()

    def listen_and_respond(self):
        print("Listening...")
        try:
            # Ensure the session is started correctly
            session_id = self.conversation.wait_for_session_end()
            print(f"Session ended with ID: {session_id}")
        except KeyboardInterrupt:
            print("Stopping...")
            self.conversation.end_session()
            sys.exit(0)

if __name__ == "__main__":
    call_agent = CallAgent()
    print("Welcome to the Call Agent! Press Ctrl+C to quit.")
    signal.signal(signal.SIGINT, lambda sig, frame: call_agent.listen_and_respond())
    call_agent.listen_and_respond()