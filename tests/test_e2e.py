from type.user_info import UserInfo
from agents.match import MatchAgent
from agents.chat import ChatAgent
from utils.utils_func import get_dummy_users_db, get_dummy_call_history


def test_e2e():
    # System pre-requisites. Users DB
    users_db = get_dummy_users_db()

    # 1. Login via LinkedIn
    query_user = UserInfo(firstname="Daniel", age=38, gender="Male", location="New York")

    # 2. Set persona

    # 3. Call with CallAgent
    call_history = get_dummy_call_history()

    # 4. Match with MatchAgent
    match_agent = MatchAgent()
    result = match_agent.match(query_user, users_db, call_history)
    print(result)
    breakpoint()

    # 5. Chat with ChatAgent
    chat_agent = ChatAgent()
    
    print("Welcome to the Eleven AI! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = chat_agent.chat(user_input)
        print(f"AI: {response}")


