import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from backend.config import GMAIL_SCOPES, GMAIL_CREDENTIALS_FILE

TOKEN_FILE = "token.json"

def get_gmail_service():
    """
    Handles OAuth2 authentication and returns an authenticated Gmail service.
    First run opens a browser for Google login — after that token.json handles it.
    """
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, GMAIL_SCOPES)

    # If no valid token, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def fetch_emails(max_results=10, query="is:unread"):
    """
    Fetch emails from Gmail inbox.
    query: Gmail search query — same syntax as Gmail search bar
    """
    service = get_gmail_service()

    # Get list of message IDs
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
        q=query
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return []

    emails = []
    for msg in messages:
        email_data = get_email_by_id(service, msg["id"])
        if email_data:
            emails.append(email_data)

    return emails


def get_email_by_id(service, msg_id):
    """
    Fetch a single email by its Gmail message ID and parse it cleanly.
    """
    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    headers = msg["payload"].get("headers", [])

    # Extract key headers
    def get_header(name):
        for h in headers:
            if h["name"].lower() == name.lower():
                return h["value"]
        return ""

    subject = get_header("Subject")
    sender  = get_header("From")
    date    = get_header("Date")
    body    = extract_body(msg["payload"])

    return {
        "id":      msg_id,
        "subject": subject,
        "sender":  sender,
        "date":    date,
        "body":    body,
        "snippet": msg.get("snippet", "")
    }


def extract_body(payload):
    """
    Recursively extract plain text body from MIME payload.
    Handles simple and multipart emails.
    """
    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                if data:
                    body += base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            elif part["mimeType"].startswith("multipart"):
                body += extract_body(part)
    else:
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return body.strip()


def send_reply(service, original_msg_id, to, subject, body):
    """
    Send a reply to an email, threading it correctly.
    """
    import email as email_lib
    from email.mime.text import MIMEText

    message = MIMEText(body)
    message["to"]      = to
    message["subject"] = f"Re: {subject}" if not subject.startswith("Re:") else subject

    # Thread the reply correctly
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent = service.users().messages().send(
        userId="me",
        body={
            "raw": raw,
            "threadId": original_msg_id
        }
    ).execute()

    return sent