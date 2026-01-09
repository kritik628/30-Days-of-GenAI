import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)
genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def chain_call(prompt, previous_context=""):
    """Professional helper to chain prompts with context."""
    full_prompt = f"{prompt}\n\nPREVIOUS CONTEXT: {previous_context}"
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=full_prompt
    )
    return response.text

# --- THE PROBLEM ---
math_problem = "Verify if the set G = {1, -1, i, -i} forms a group under complex multiplication."

print(f"🚀 Starting Chain for: {math_problem}")

# STEP 1: Axiom Identification
print("\n[Step 1: Identifying Axioms...]")
axioms = chain_call(f"List the 4 group axioms (Closure, Associativity, Identity, Inverse) needed to solve: {math_problem}")
print("✅ Axioms identified.")

# STEP 2: Mathematical Verification
print("[Step 2: Performing Step-by-Step Proof...]")
proof = chain_call("Provide a rigorous mathematical proof for each axiom using the set G provided.", axioms)
print("✅ Proof generated.")

# STEP 3: DTU Exam Formatting
print("[Step 3: Formatting for DTU Syllabus...]")
final_output = chain_call("Format this into a formal proof suitable for a DTU Modern Algebra exam paper.", proof)

print("\n--- FINAL DTU-STYLE PROOF ---")
print(final_output)