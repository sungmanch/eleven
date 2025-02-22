from type.user_info import UserInfo
from langgraph.graph import MessagesState
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
    print(call_history)

    # 4. Match with MatchAgent
    match_agent = MatchAgent()
    result = match_agent.match(query_user, users_db, call_history)
    print(result)

    # 5. Chat with ChatAgent
    chat_agent = ChatAgent(user_info=query_user)
    chat_agent.add_call_history(call_history)

    feedback_message = chat_agent.ask_feedback()
    print(feedback_message)

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = chat_agent.chat(user_input)
        print(f"Eleven: {response}")


if __name__ == "__main__":
    test_e2e()
