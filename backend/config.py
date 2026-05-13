import base64
import os
import sys
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY         = os.getenv("GEMINI_API_KEY")
GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
DATABASE_URL           = os.getenv("DATABASE_URL", "sqlite:///./emails.db")
GEMINI_MODEL           = "gemini-3-flash-preview"

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

# Restore credentials.json from environment variable (for Render deployment)
creds_b64 = os.getenv("GMAIL_CREDENTIALS_B64")
if creds_b64 and not os.path.exists("credentials.json"):
    with open("credentials.json", "w") as f:
        f.write(base64.b64decode(creds_b64).decode())
    print("✅ credentials.json restored from environment")

# Restore token.json from environment variable (for Render deployment)
token_b64 = os.getenv("GMAIL_TOKEN_B64")
if token_b64 and not os.path.exists("token.json"):
    with open("token.json", "w") as f:
        f.write(base64.b64decode(token_b64).decode())
    print("✅ token.json restored from environment")

# Validate required keys
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY is missing!")
    sys.exit(1)