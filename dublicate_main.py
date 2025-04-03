from email_fetcher import authenticate_gmail, fetch_emails
from llm_integration import generate_email_response_gemini
from tool_integrations import send_slack_message, schedule_calendar_event
from database import init_db, insert_email

def main():
    # Initialize database
    init_db()

    # Authenticate and fetch emails (limit to 10 emails)
    service = authenticate_gmail()
    emails = fetch_emails(service, query="is:unread")[:10]  # Get only the first 10 emails
    
    # Process each email
    for email in emails:
        print("Processing email:", email.get('subject'))
        # Store email in the database
        insert_email(email)
        
        # Generate a draft response using LLM
        prompt = f"Draft a reply to the following email: {email.get('snippet')}"
        draft_reply = generate_email_response_gemini(prompt)
        print("Draft reply:", draft_reply)
        
        # Example tool integrations:
        # If the email is from a certain sender, send a Slack notification
        if "important" in email.get('subject', '').lower():
            send_slack_message(f"Important email received: {email.get('subject')}")
        
        # Example: If the email mentions a meeting, schedule a calendar event
        if "meeting" in email.get('snippet', '').lower():
            schedule_calendar_event({"title": email.get('subject'), "date": "2025-04-05"})
        
    print("Processing complete.")

if __name__ == '__main__':
    main()
