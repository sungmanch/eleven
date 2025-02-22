import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from type.user_info import UserInfo


class ChatAgent:
    def __init__(self, user_info: UserInfo):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.0,
            top_p=1.0,
            n=1,
        )
        self.graph = StateGraph(state_schema=MessagesState)

        self.graph.add_edge(START, "model")
        self.graph.add_node("model", self.call_model)

        self.memory = MemorySaver()
        self.app = self.graph.compile(checkpointer=self.memory)

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
        previous_messages = state.get("messages", [])
        current_messages = state["messages"]

        if self.is_first_message:
            previous_messages = previous_messages + self.call_history
            self.is_first_message = False
        
        system_prompt = SystemMessage(
            content=(
                "Your main objective is to help the user find a match. "
                "You will be given a list of users and a call history. "
                "You will need to find the best match for the user based on the call history. "
                "You will need to return the name of the user that is the best match. "
                "During overall process, don't forget to be friendly and cheerful."
                "You are a friendly AI assistant named Eleven."
                "Casual and friendly tone is mandatory."
            )
        )
        all_messages = [system_prompt] + previous_messages + current_messages
        
        response = self.llm.invoke(all_messages)
        
        state["messages"] = all_messages + [response]

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
