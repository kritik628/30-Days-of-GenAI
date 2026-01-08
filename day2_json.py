import os
from google import genai
from dotenv import load_dotenv
import json
# The 'override=True' forces Python to re-read the .env file 
# and replace any old keys stored in memory.
load_dotenv(override=True) 

api_key = os.getenv("GEMINI_API_KEY")

# Temporary check: Run this to see what key is actually being used
print(f"--- DEBUG: Key starts with {api_key[:10]} ---")

client = genai.Client(api_key=api_key)


messy_input = """
Hey guys, big news! Microsoft is visiting DTU on February 15th. 
They are hiring for the 'Applied AI Engineer' role. 
The stipend is 1.5 Lakh per month for the internship! 
Apply by Jan 30th.
"""

# Day 2: Advanced JSON with Error Handling
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": "Extract: company, role, stipend, deadline. Return ONLY valid JSON.",
            "response_mime_type": "application/json" 
        },
        contents=messy_input
    )

    extracted_data = json.loads(response.text)
    
    print("✅ EXTRACTION SUCCESSFUL:")
    # Using .get() prevents the crash if a key is missing
    print(f"Company: {extracted_data.get('company', 'N/A')}")
    print(f"Role: {extracted_data.get('role', 'N/A')}")
    print(f"Stipend: {extracted_data.get('stipend', 'N/A')}")
    print(f"Deadline: {extracted_data.get('deadline', 'N/A')}")

except Exception as e:
    print(f"❌ Error: {e}")