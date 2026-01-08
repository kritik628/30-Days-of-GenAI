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

# Each message must be a 'Content' object with a 'role' and 'parts'
history = [
    types.Content(
        role="user",
        parts=[types.Part(text="Hi, I'm ready for the interview.")]
    ),
    types.Content(
        role="model",
        parts=[types.Part(text="Welcome. I am a Senior AI Engineer at Google. State your name and your most proud AI project.")]
    )
]

# 2. System Instruction stays separate
system_instruction = "You are a tough Google Interviewer. Only discuss AI and technical engineering."

print("--- GOOGLE INTERVIEW SIMULATOR START ---")
print("Interviewer: Welcome. State your name and your most proud AI project.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    # Add user message to history
    history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
    
    # 3. Send the entire history to maintain memory
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_instruction),
        contents=history
    )
    
    # Add AI response to history
    history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
    
    print(f"\nGoogle Interviewer: {response.text}")
    print(f"\n[DEBUG] Context length: {len(history)} messages")
    print("-" * 30)