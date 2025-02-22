from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

class ChatAgent:
    def __init__(self, user_info):
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
        app = self.graph.compile(saver=self.memory)

    def call_model(self, state: MessagesState):
        response = self.llm.invoke(state["messages"])
        return {"messages": response}

    def chat(self, call_history: str, user_info: dict):
        system_prompt = "You are a helpful assistant."
        user_prompt = f"call history:{call_history}\nuser info:{user_info}"
        prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = self.llm.invoke(prompt)  # type: ignore
        return response

    def _find_best_match(self, call_history: str, user_info: dict):
        pass

    def get_response(self, message):
        pass