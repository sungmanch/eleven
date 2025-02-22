import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from type.user_info import UserInfo

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface


class ChatAgent:
    def __init__(self, user_info: UserInfo):
        # Initialize ElevenLabs client and conversation
        api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=api_key)
        self.conversation = Conversation(
            self.client,
            agent_id="GExUCktNNwJ82r2Nrlbs",
            requires_auth=bool(api_key),
            audio_interface=DefaultAudioInterface(),
            callback_agent_response=lambda response: print(f"Agent: {response}"),
            callback_agent_response_correction=lambda original, corrected: print(
                f"Agent: {original} -> {corrected}"
            ),
            callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
        )
        self.conversation.start_session()

        self.user_info = user_info
        self.config = {
            "configurable": {
                "thread_id": self.user_info.id,
            }
        }

        self.call_history = ""
        self.is_first_message = True
    
    def add_call_history(self, call_history: str):
        self.call_history = call_history

    def call_model(self, state: MessagesState):
        # Use ElevenLabs conversation to generate responses
        user_input = state.get("messages", [])[-1].content
        self.conversation.send_message(user_input)
        response = self.conversation.wait_for_response()
        state["messages"].append(response)
        return {"messages": response}

    def chat(self, message: str):
        query = message
        input_messages = [HumanMessage(content=query)]
        output = self.app.invoke({"messages": input_messages}, self.config)
        return output["messages"][-1].content

    def ask_feedback(self):
        query = (
            "could you please make catch up message to the user?"
            "Based on the previous messages, you need to make a catch up message to the user."
            "You are a friendly AI assistant named Eleven."
            "Casual and friendly tone is mandatory."
        )
        input_messages = [HumanMessage(content=query)]
        output = self.app.invoke({"messages": input_messages}, self.config)
        return output["messages"][-1].content

if __name__ == "__main__":
    user_info = UserInfo(name="Bob", age=25, gender="male", location="New York", id="123")
    chat_agent = ChatAgent(user_info)
    
    print("Welcome to the Chat App! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = chat_agent.chat(user_input)
        print(f"Eleven: {response}")
