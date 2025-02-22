import json
from type.user_info import UserInfo

def get_dummy_users_db() -> list[UserInfo]:
    with open("dummy_user_db.json", "r") as f:
        users_data = json.load(f)
        return [UserInfo(**user) for user in users_data]
    
def get_dummy_call_history() -> str:
    with open("dummy_call_history.json", "r") as f:
        call_history_data = json.load(f)
        transcript = call_history_data.get("transcript", [])
        messages = [entry["message"] for entry in transcript if entry["message"] is not None]
        return messages