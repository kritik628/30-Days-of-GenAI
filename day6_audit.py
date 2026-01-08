import os
import time
from google import genai
from google.genai import errors # We need this to catch specific API errors
from dotenv import load_dotenv

load_dotenv(override=True)
genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print(f"✅ Ready. Using Key: {os.getenv('GEMINI_API_KEY')[:10]}...")

# HFT FAILOVER STRATEGY: 1.5-flash is the most reliable for high-frequency testing
models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]

def safe_generate(prompt):
    for model_name in models_to_try:
        try:
            print(f"🚀 Attempting with: {model_name}...")
            response = genai_client.models.generate_content(
                model=model_name, 
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Capture the error message to check for Quota or Overload
            err_msg = str(e).lower()
            if "429" in err_msg or "quota" in err_msg or "503" in err_msg or "overloaded" in err_msg:
                print(f"⚠️ {model_name} hit a limit. Failing over to next model...")
                time.sleep(2) # Brief pause to allow the API to breathe
                continue
            else:
                # If it's a different error (like a typo), we want to see it
                print(f"❌ Unexpected Error: {e}")
                raise e
    
    return "🛑 SYSTEM ALERT: All models have reached their limits. Wait 60 seconds."

# --- DAY 6 EXECUTION ---

# Step 1: The 'Developer'
print("\n[AI Developer is writing code...]")
generated_code = safe_generate("Write a Python function to connect to a database using a password.")

if "SYSTEM ALERT" in generated_code:
    print(generated_code)
else:
    print("--- DEVELOPER OUTPUT ---")
    print(generated_code)

    # Step 2: The 'Auditor'
    print("\n[AI Auditor is reviewing code...]")
    audit_prompt = f"Review this code for hardcoded secrets and logic errors:\n{generated_code}"
    audit_report = safe_generate(audit_prompt)

    print("\n--- SECURITY AUDIT REPORT ---")
    print(audit_report)