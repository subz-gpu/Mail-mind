import re
import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess_email(email: dict) -> dict:
    """
    Clean and extract structured info from raw email.
    Returns enriched email dict ready for Gemini.
    """
    body = email.get("body", "") or email.get("snippet", "")

    # Step 1 — Strip HTML tags
    body = re.sub(r'<[^>]+>', '', body)

    # Step 2 — Remove quoted replies (everything after "On ... wrote:")
    body = re.sub(r'On .+? wrote:.*', '', body, flags=re.DOTALL)

    # Step 3 — Remove email signatures (lines after "--" or "Regards,")
    body = re.sub(r'(--|__|\bRegards\b|\bThanks\b|\bSincerely\b).*', '', body, flags=re.DOTALL | re.IGNORECASE)

    # Step 4 — Collapse extra whitespace
    body = re.sub(r'\n{3,}', '\n\n', body)
    body = body.strip()

    # Step 5 — spaCy NER (Named Entity Recognition)
    doc = nlp(body)
    entities = [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
    ]

    # Step 6 — Detect intent using keywords
    intent = detect_intent(body)

    # Step 7 — Detect tone/urgency
    urgency = detect_urgency(body)

    return {
        **email,
        "clean_body": body,
        "entities": entities,
        "intent": intent,
        "urgency": urgency,
        "word_count": len(body.split())
    }


def detect_intent(text: str) -> str:
    """
    Rule-based intent detection from email body.
    """
    text_lower = text.lower()

    intent_keywords = {
        "complaint":        ["complaint", "issue", "problem", "not working", "broken", "disappointed", "frustrated", "wrong"],
        "meeting_request":  ["meeting", "schedule", "call", "appointment", "available", "catch up", "discuss"],
        "inquiry":          ["question", "query", "wondering", "would like to know", "can you", "could you", "information"],
        "follow_up":        ["follow up", "following up", "checking in", "just wanted", "reminder", "any update"],
        "thank_you":        ["thank you", "thanks", "grateful", "appreciate", "appreciated"],
        "job_application":  ["apply", "application", "resume", "cv", "position", "vacancy", "opportunity"],
        "escalation":       ["urgent", "asap", "immediately", "escalate", "critical", "emergency"],
    }

    for intent, keywords in intent_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return intent

    return "general"


def detect_urgency(text: str) -> str:
    """
    Detect urgency level from email body.
    """
    text_lower = text.lower()

    high_urgency    = ["urgent", "asap", "immediately", "emergency", "critical", "right away"]
    medium_urgency  = ["soon", "at your earliest", "when possible", "by tomorrow", "by end of day"]

    if any(word in text_lower for word in high_urgency):
        return "high"
    elif any(word in text_lower for word in medium_urgency):
        return "medium"
    return "normal"