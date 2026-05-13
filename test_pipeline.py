from backend.utils.gmail import fetch_emails
from backend.utils.preprocessor import preprocess_email
from backend.utils.gemini import generate_reply, generate_reply_variants

print("Fetching emails...")
emails = fetch_emails(max_results=3, query="is:unread")

if not emails:
    print("No unread emails found. Trying inbox instead...")
    emails = fetch_emails(max_results=3, query="in:inbox")

for email in emails[:1]:  # Test with just the first email
    print("\n" + "="*60)
    print(f"FROM:    {email['sender']}")
    print(f"SUBJECT: {email['subject']}")
    print(f"BODY:    {email['body'][:200]}...")

    # Step 1 — Preprocess
    print("\n--- PREPROCESSING ---")
    processed = preprocess_email(email)
    print(f"Intent:   {processed['intent']}")
    print(f"Urgency:  {processed['urgency']}")
    print(f"Entities: {processed['entities'][:5]}")

    # Step 2 — Generate reply
    print("\n--- GENERATING REPLY ---")
    result = generate_reply(processed, tone="professional")
    print(f"\nREPLY:\n{result['reply']}")

    # Step 3 — Generate 3 tone variants
    print("\n--- 3 TONE VARIANTS ---")
    variants = generate_reply_variants(processed)
    for tone, reply in variants['variants'].items():
        print(f"\n[{tone.upper()}]\n{reply}")
        print("-"*40)