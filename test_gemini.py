import sys
sys.path.insert(0, 'backend')

from config import GEMINI_API_KEY, GEMINI_MODEL
from google import genai

print("API Key:", GEMINI_API_KEY[:15] if GEMINI_API_KEY else "MISSING!")
print("Model:", GEMINI_MODEL)

client = genai.Client(api_key=GEMINI_API_KEY)

try:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Say hello in one sentence."
    )
    print("✅ Gemini working:", response.text)
except Exception as e:
    print("❌ Gemini error:", str(e))