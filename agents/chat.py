from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage



class ChatAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.0,
            top_p=1.0,
            n=1,
        )

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