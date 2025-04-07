
from datetime import datetime
from email_fetcher import authenticate_gmail, fetch_emails
from calendar_utils import schedule_calendar_event
from llm_integration import generate_email_response_gemini
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database import init_db, insert_email
from tool_integrations import send_slack_message, is_meeting_related, extract_datetime_from_email

def main():
    # Initialize database
    init_db()

    # Authenticate and fetch primary unread emails (limit to 10)
    service = authenticate_gmail()
    query = "in:inbox category:primary is:unread"
    emails = fetch_emails(service, query=query)[:10]

    for email in emails:
        print(f" Processing email: {email.get('subject')}")
        insert_email(email)
        if is_meeting_related(email.get('snippet', '')):
            # Extract datetime object directly
            email_snippet = email.get('snippet', '')
            print(f" Raw email snippet: {email_snippet}")
            #extract the meeting time and put in the variable to used 
            meeting_datetime = extract_datetime_from_email(email_snippet)
            print(f" Extracted datetime: {meeting_datetime}")
            if meeting_datetime:
                try:
                    start_datetime = meeting_datetime.strftime("%Y-%m-%dT%H:%M:%S")
                    print(f" Final start_datetime: {start_datetime}")

                    schedule_calendar_event({
                        'title': email.get('subject', 'Meeting'),
                        'start_datetime': start_datetime
                    })

                except ValueError as e:
                    print(f" Error formatting date/time: {e}")
            else:
                print(" No meeting found on mail. Skipping this email.")



            # Generate a reply to the email (optional)
            prompt = f"Draft a reply to the following email: {email.get('snippet')}"
            draft_reply = generate_email_response_gemini(prompt)
            print(f" Draft Reply: {draft_reply}")

        # Send the email details to Slack for all processed emails
        send_slack_message(f" New Email: {email.get('subject')}\n{email.get('snippet')}")

    print(" Processing complete.")

if __name__ == "__main__":
    main()
