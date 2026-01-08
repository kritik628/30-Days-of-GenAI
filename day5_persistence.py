import json
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types


# The 'override=True' forces Python to re-read the .env file 
# and replace any old keys stored in memory.
load_dotenv(override=True) 

api_key = os.getenv("GEMINI_API_KEY")

# Temporary check: Run this to see what key is actually being used
print(f"--- DEBUG: Key starts with {api_key[:10]} ---")

client = genai.Client(api_key=api_key)






HISTORY_FILE = "chat_history.json"

# 1. LOAD: Opening the drawer and reading the old file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            raw_data = json.load(f)
            # Turning the text back into 'AI-readable' objects
            return [types.Content(role=item['role'], 
                                 parts=[types.Part(text=item['parts'][0]['text'])]) 
                    for item in raw_data]
    return []

# 2. SAVE: Writing the new conversation into the drawer
def save_history(history):
    # Turning the 'AI objects' into simple text for the file
    serializable_history = [
        {"role": h.role, "parts": [{"text": h.parts[0].text}]} 
        for h in history
    ]
    with open(HISTORY_FILE, "w") as f:
        json.dump(serializable_history, f, indent=4)

# --- THE ACTUAL PROGRAM ---
history = load_history()
print(f"--- WELCOME BACK: Loaded {len(history)} past messages ---")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant who remembers the user."
            ),
            contents=history
        )
        
        history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
        print(f"\nAI: {response.text}")
        
        # 3. SAVE after every single message
        save_history(history)
        
    except Exception as e:
        print(f"Error: {e}. (If 503, just wait 1 minute)")