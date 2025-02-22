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
        
        all_messages = previous_messages + current_messages
        response = self.llm.invoke(all_messages)
        
        state["messages"] = all_messages + [response]

        return {"messages": response}

    def chat(self, message: str):
        query = message
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
