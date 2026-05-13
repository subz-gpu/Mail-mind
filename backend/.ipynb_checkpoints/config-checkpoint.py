from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./emails.db")

# Gmail API scopes — read and send access
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

# Gemini model to use
GEMINI_MODEL = "gemini-3-flash-preview"