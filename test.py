import google.generativeai as genai
import os

# 1. Setup your API Key
# Replace 'YOUR_API_KEY' with your actual key, or use os.getenv("GEMINI_API_KEY")
api_key = os.getenv("GEMINI_API_KEY") or "AIzaSyBJnY3k6wJz3WvUubQ17Op_7OKRhZsggf0"
genai.configure(api_key=api_key)

print("Fetching available Gemini models...\n")

try:
    # 2. List all models
    for m in genai.list_models():
        # 3. Filter for models that support content generation (chat/text)
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
            print(f"Display Name: {m.display_name}")
            print(f"Description: {m.description}")
            print("-" * 40)
            
except Exception as e:
    print(f"Error fetching models: {e}")