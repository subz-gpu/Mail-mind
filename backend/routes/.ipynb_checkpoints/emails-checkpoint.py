from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db, EmailHistory
from backend.utils.gmail import fetch_emails, get_gmail_service, send_reply
from backend.utils.preprocessor import preprocess_email
from backend.utils.gemini import generate_reply, generate_reply_variants
import uuid

router = APIRouter()


# ── Request models ──────────────────────────────────────────
class GenerateReplyRequest(BaseModel):
    email_id:   str
    tone:       Optional[str] = "professional"
    generate_variants: Optional[bool] = False

class SendReplyRequest(BaseModel):
    email_id:   str
    to:         str
    subject:    str
    reply_body: str


# ── GET /emails ──────────────────────────────────────────────
@router.get("/emails")
def get_emails(max_results: int = 10, query: str = "is:unread"):
    """
    Fetch emails from Gmail inbox.
    """
    try:
        emails = fetch_emails(max_results=max_results, query=query)
        if not emails:
            emails = fetch_emails(max_results=max_results, query="in:inbox")
        return {"emails": emails, "count": len(emails)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /generate-reply ─────────────────────────────────────
@router.post("/generate-reply")
def generate_reply_endpoint(
    request: GenerateReplyRequest,
    db: Session = Depends(get_db)
):
    """
    Preprocess an email and generate an AI reply using Gemini.
    """
    try:
        # Fetch the specific email
        service = get_gmail_service()
        from backend.utils.gmail import get_email_by_id
        email = get_email_by_id(service, request.email_id)

        if not email:
            raise HTTPException(status_code=404, detail="Email not found")

        # Preprocess
        processed = preprocess_email(email)

        # Generate reply
        if request.generate_variants:
            result = generate_reply_variants(processed)
        else:
            result = generate_reply(processed, tone=request.tone)

        # Save to database
        history = EmailHistory(
            id         = str(uuid.uuid4()),
            sender     = email.get("sender", ""),
            subject    = email.get("subject", ""),
            body       = processed.get("clean_body", ""),
            intent     = processed.get("intent", ""),
            urgency    = processed.get("urgency", ""),
            reply      = result.get("reply", "") if not request.generate_variants
                         else str(result.get("variants", {})),
            tone       = request.tone
        )
        db.add(history)
        db.commit()

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /send-reply ─────────────────────────────────────────
@router.post("/send-reply")
def send_reply_endpoint(request: SendReplyRequest):
    """
    Send a reply email via Gmail.
    """
    try:
        service = get_gmail_service()
        result = send_reply(
            service,
            original_msg_id = request.email_id,
            to              = request.to,
            subject         = request.subject,
            body            = request.reply_body
        )
        return {"success": True, "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /history ─────────────────────────────────────────────
@router.get("/history")
def get_history(db: Session = Depends(get_db), limit: int = 20):
    """
    Fetch past generated replies from SQLite.
    """
    records = db.query(EmailHistory)\
                .order_by(EmailHistory.created_at.desc())\
                .limit(limit).all()

    return {
        "history": [
            {
                "id":         r.id,
                "sender":     r.sender,
                "subject":    r.subject,
                "intent":     r.intent,
                "urgency":    r.urgency,
                "tone":       r.tone,
                "reply":      r.reply,
                "created_at": r.created_at.isoformat()
            }
            for r in records
        ]
    }