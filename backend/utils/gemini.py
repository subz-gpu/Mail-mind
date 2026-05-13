from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

TONE_INSTRUCTIONS = {
    "professional": "formal, polished, and business-appropriate",
    "friendly":     "warm, approachable, and conversational",
    "concise":      "brief, direct, and to the point — under 80 words",
    "empathetic":   "understanding, caring, and supportive",
    "assertive":    "confident, clear, and action-oriented",
}


def generate_reply(email: dict, tone: str = "professional") -> dict:
    tone_desc  = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["professional"])
    intent     = email.get("intent", "general")
    urgency    = email.get("urgency", "normal")
    entities   = email.get("entities", [])
    clean_body = email.get("clean_body", email.get("body", ""))
    sender     = email.get("sender", "the sender")
    subject    = email.get("subject", "")

    entity_str = ""
    if entities:
        entity_str = "Key entities detected: " + ", ".join(
            f"{e['text']} ({e['label']})" for e in entities[:8]
        )

    prompt = f"""You are a professional email assistant. Generate a reply to the following email.

EMAIL DETAILS:
- From: {sender}
- Subject: {subject}
- Intent: {intent}
- Urgency: {urgency}
{entity_str}

EMAIL BODY:
{clean_body}

INSTRUCTIONS:
- Tone: {tone_desc}
- Address the sender's intent directly and completely
- If urgency is high, acknowledge it at the start
- Be natural — do not sound robotic or templated
- Do not make up facts, dates, or commitments not in the email
- End with a clear next step or closing
- Do not include a subject line in your reply
- Start directly with the greeting (e.g. "Dear..." or "Hi...")

REPLY:"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    reply_text = response.text.strip()

    return {
        "original_email": email,
        "reply": reply_text,
        "tone": tone,
        "intent": intent,
        "urgency": urgency
    }


def generate_reply_variants(email: dict) -> dict:
    tones = ["professional", "friendly", "concise"]
    variants = {}

    for tone in tones:
        result = generate_reply(email, tone=tone)
        variants[tone] = result["reply"]

    return {
        "original_email": email,
        "variants": variants,
        "intent": email.get("intent"),
        "urgency": email.get("urgency")
    }