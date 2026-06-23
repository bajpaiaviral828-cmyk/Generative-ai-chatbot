import os
import sys
from dotenv import load_dotenv

from chatbot.core import ChatBot
from chatbot.persistence import SimpleJSONSaver

# I read that it's good practice to load .env so my keys don't leak on github
load_dotenv()

def main():
    print("=============================================")
    print("🤖 My First Generative AI Chatbot")
    print("=============================================")
    print("Type 'quit' or 'exit' to stop.")
    print("Type '/reset' to start a new conversation.")
    print("=============================================\n")

    # this handles saving and loading the chats to a json file
    backend = SimpleJSONSaver(filename="my_saved_chats.json")
    
    # just hardcoding a session id for now until I build a multi-user login system
    bot = ChatBot(session_id="student_user", backend=backend)

    print(f"Loaded previous chat! (Current turns: {bot.get_turn_count()})")

    while True:
        try:
            # wait for me to type
            user_input = input("\nYou: ")
            
            # check if I want to quit
            if user_input.lower() in ['quit', 'exit']:
                print("Bye! Saving chats...")
                break
            
            # check if I want to wipe the memory
            if user_input.lower() == '/reset':
                bot.reset()
                print(">> Memory wiped! Started a new chat.")
                continue

            # otherwise, send the message to gemini
            response = bot.send(user_input)
            print(f"\nBot: {response}")

        except KeyboardInterrupt:
            # this catches if I press Ctrl+C in the terminal
            print("\nExiting...")
            break
        except Exception as e:
            # FIXME: figure out why this sometimes throws weird parsing errors
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    main()
