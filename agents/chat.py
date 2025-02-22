from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

if TYPE_CHECKING:
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
        self.app = self.graph.compile(saver=self.memory)

        self.user_info = user_info
        self.config = {
            "configurable": {
                "user_id": self.user_info.id,
            }
        }

    def call_model(self, state: MessagesState):
        response = self.llm.invoke(state["messages"])
        return {"messages": response}

    def chat(self, message: str):
        query = message
        input_messages = [HumanMessage(query)]
        output = self.app.invoke({"messages": input_messages}, self.config)
        return output["messages"][-1].content
