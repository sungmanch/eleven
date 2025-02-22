import json

from type.user_info import UserInfo
from langchain_openai import ChatOpenAI

class MatchAgent:
    def __init__(self):
        self.users_db = self._load_users_db()
        self.call_history = self._get_chat_history()
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.75,
        )

    def match(
        self, 
        user_info: UserInfo, 
        users_db: list[UserInfo],
        call_history: list[str],
    ):
        system_prompt = (
            "You are a match agent. You are given a user's information and a list of users. "
            "You need to match the user with the list of users. "
        )
        user_prompt = (
            f"User's information: {user_info}\n"
            f"List of users: {users_db}\n"
            f"Call history: {call_history}\n"
        )
        prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = self.llm.invoke(prompt)
        return response.content

if __name__ == "__main__":
    match_agent = MatchAgent()
    user_info = UserInfo(firstname="Daniel", age=38, gender="Male", location="New York")

