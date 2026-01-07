import os
import sys
from langchain_core.messages import HumanMessage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

try:
    from langchain_community.chat_message_histories import RedisChatMessageHistory
    print("Using langchain_community.chat_message_histories")
except ImportError as e:
    print(f"Community NOT FOUND: {e}")
    sys.exit(1)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def verify():
    print(f"Testing RedisChatMessageHistory with URL: {REDIS_URL}")
    try:
        # langchain_community uses 'url'
        history = RedisChatMessageHistory(
            session_id="test-verify-comm",
            url=REDIS_URL,
            key_prefix="verify-comm:"
        )
        
        print("Adding message...")
        history.add_message(HumanMessage(content="Hello Community"))
        
        print("Retrieving messages...")
        msgs = history.messages
        print(f"Retrieved {len(msgs)} messages.")
        for m in msgs:
            print(f"- {m.content}")
            
        if len(msgs) > 0 and "Hello Community" in [m.content for m in msgs]:
            print("SUCCESS")
        else:
            print("FAILURE")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    verify()