
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

print("--- CONNECTING TO GEMINI 2.5 FLASH ---")

try:
    # Use the EXACT string from your list
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents="I am Kritik from DTU. Confirm you are online and ready for Day 2."
    )

    print("✅ SUCCESS! Day 1 is officially complete.")
    print(f"🤖 AI RESPONSE: {response.text}")

except Exception as e:
    print(f"❌ ERROR: {e}")