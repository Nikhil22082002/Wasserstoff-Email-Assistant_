import re
import dateparser
from datetime import datetime 
from email_fetcher import authenticate_gmail, fetch_emails
from calendar_utils import schedule_calendar_event
from llm_integration import generate_email_response_gemini
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database import init_db, insert_email
from tool_integrations import send_slack_message, is_meeting_related, extract_date_and_time_from_email

def main():
    # Initialize database
    init_db()

    # Authenticate and fetch primary unread emails (limit to  5)
    service = authenticate_gmail()
    query = "in:inbox category:primary is:unread"
    emails = fetch_emails(service, query=query)[:5]

    for email in emails:
        print(f"📩 Processing email: {email.get('subject')}")
        insert_email(email)
        # Generate the reply with the help of gimin api
        prompt = f"Draft a reply to the following email: {email.get('snippet')}"
        draft_reply = generate_email_response_gemini(prompt)
        print(f"✉️ Draft Reply: {draft_reply}")
        # Check if email is about scheduling a meeting
        if is_meeting_related(email.get('snippet', '')):
    
    # Extract date and time from email
            meeting_date = extract_date_and_time_from_email(email.get('snippet', ''))
            if meeting_date and meeting_date[0] and meeting_date[1]:
                date, time = meeting_date
                try:
                    combined_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
                    start_datetime = combined_datetime.strftime("%Y-%m-%dT%H:%M:%S")
                    print(f"✅ Final start_datetime: {start_datetime}")
                    schedule_calendar_event({
                        'title': email.get('subject', 'Meeting'),
                        'start_datetime': start_datetime
                    })
                except ValueError as e:
                    print(f"❌ Error parsing date/time: {e}")
            else:
                print("⏳ No  Meeting  found. Skipping this email.")
    
      
        # Send the email details to Slack for all processed emails
        send_slack_message(f"📧 New Email: {email.get('subject')}\n{email.get('snippet')}")

    print("✅ Processing complete.")

if __name__ == "__main__":
    main()
