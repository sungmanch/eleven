import json

from type.user_info import UserInfo
from langchain_openai import ChatOpenAI

class MatchAgent:
    def __init__(self):
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
            "You are a match agent. You are given a user's information and a list of users and call history. "
            "You need to match the user with the list of users. "
            "Please return the user profile card in JSON format and reason why you choose this user."
            "When you are matching, you need to consider the user's information and the call history."
            "Think step by step and reason why you choose this user."
            "Example of user profile card: "
            "{"
                "name: John Doe, "
                "age: 30, "
                "gender: Male, "
                "location: New York, "
                "job: Software Engineer, "
                "reason: He is a good match because he is a software engineer and he is from New York."
            "}"
            "Do not include any other information except the user profile card."
            "Do not include ````json` or ```` return format should be string."
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

