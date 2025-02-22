from agents.chat import ChatAgent
from type.user_info import UserInfo

user_info = UserInfo(name="Bob", age=25, gender="male", location="New York", id="123")
chat_agent = ChatAgent(user_info)

print(chat_agent.chat("Hi! I'm Bob."))
