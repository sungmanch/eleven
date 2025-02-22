import os
import signal

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

agent_id = "GExUCktNNwJ82r2Nrlbs"
api_key = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(api_key=api_key)

conversation = Conversation(
    client,
    agent_id,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(
        f"Agent: {original} -> {corrected}"
    ),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
)

conversation.start_session()

signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
conversation_id = conversation.wait_for_session_end()
print(f"Conversation ID: {conversation_id}")

if __name__ == "__main__":
    print("Welcome to the ElevenLabs Chat App! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        # Here you would integrate the logic to send user_input to the ElevenLabs API and get a response
        # For now, we will just simulate a response
        response = "This is a simulated response from ElevenLabs."
        print(f"Eleven: {response}") 