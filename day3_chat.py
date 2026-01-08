import os
from google import genai
from dotenv import load_dotenv

# The 'override=True' forces Python to re-read the .env file 
# and replace any old keys stored in memory.
load_dotenv(override=True) 

api_key = os.getenv("GEMINI_API_KEY")

# Temporary check: Run this to see what key is actually being used
print(f"--- DEBUG: Key starts with {api_key[:10]} ---")

client = genai.Client(api_key=api_key)
# Start a 'chat' instead of a single 'generate_content' call
chat = client.chats.create(model="gemini-2.5-flash")

print("--- DTU AI ASSISTANT START (Type 'exit' to stop) ---")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
        
    response = chat.send_message(user_input)
    print(f"AI: {response.text}")