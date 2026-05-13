from backend.utils.gmail import fetch_emails

emails = fetch_emails(max_results=5, query="is:unread")

for email in emails:
    print("─" * 50)
    print(f"From:    {email['sender']}")
    print(f"Subject: {email['subject']}")
    print(f"Date:    {email['date']}")
    print(f"Body:    {email['body'][:200]}...")