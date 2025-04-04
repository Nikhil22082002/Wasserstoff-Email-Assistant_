import re
import dateparser
from email_fetcher import authenticate_gmail, fetch_emails
from calendar_utils import schedule_calendar_event, propose_alternative_time
from llm_integration import generate_email_response_gemini
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database import init_db, insert_email
from tool_integrations import send_slack_message,is_meeting_related
# Function to extract date from the email content

def extract_date_from_email(snippet):
    date = dateparser.parse(snippet)
    if date:
        return date.isoformat()
    return None

# Main logic to process emails and handle meeting scheduling
def main():
    # Initialize database
    init_db()

    # Authenticate and fetch emails (limit to 5)
    service = authenticate_gmail()
    emails = fetch_emails(service, query="is:unread")[:5]

    for email in emails:
        print(f"📩 Processing email: {email.get('subject')}")
        insert_email(email)

        # Check if email is about scheduling a meeting
        if is_meeting_related(email.get('snippet', '')):
            # Extract date from email snippet (e.g., "meeting on Friday")
            meeting_date = extract_date_from_email(email.get('snippet', ''))

            # If a date is found, schedule the event
            if meeting_date:
                print(f"📅 Found meeting date: {meeting_date}")
                schedule_calendar_event({
                    'title': email.get('subject'),
                    'date': meeting_date,
                })
            else:
                # If no date is found, propose an alternative time
                print("⏳ No specific date found. Proposing alternative time.")
                propose_alternative_time(email)
            
            # Generate a reply to the email (optional, depending on use case)
            prompt = f"Draft a reply to the following email: {email.get('snippet')}"
            draft_reply = generate_email_response_gemini(prompt)
            print(f"✉️ Draft Reply: {draft_reply}")
            send_slack_message(f"📧 New Email: {email.get('subject')}\n{email.get('snippet')}")

    print("✅ Processing complete.")

if __name__ == "__main__":
    main()
