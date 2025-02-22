import json

from type.user_info import UserInfo

class MatchAgent:
    def __init__(self):
        self.users_db = self._load_users_db()

    def _load_users_db(self) -> list[UserInfo]:
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
