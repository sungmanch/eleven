import json

from type.user_info import UserInfo
from langchain_openai import ChatOpenAI

class MatchAgent:
    def __init__(self):
        self.users_db = self._load_users_db()
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.75,
        )

    def _load_users_db(self) -> list[UserInfo]:
        #TODO: Need to change to actual db
        with open("dummy_user_db.json", "r") as f:
            users_data = json.load(f)
            return [UserInfo(**user) for user in users_data]

    def match(
        self, 
        user_info: UserInfo, 
        users_db: list[UserInfo],
        call_history: list[str],
    ):
        pass

if __name__ == "__main__":
    match_agent = MatchAgent()
    user_info = UserInfo(firstname="Daniel", age=38, gender="Male", location="New York")