from agents.chat import ChatAgent
from type.user_info import UserInfo

def test_chat_agent():
    user_info = UserInfo(name="Bob", age=25, gender="male", location="New York", id="123")
    chat_agent = ChatAgent(user_info)
    
    response = chat_agent.chat("Hi! I'm Bob.")
    assert response is not None  # Add more specific assertions based on expected behavior
