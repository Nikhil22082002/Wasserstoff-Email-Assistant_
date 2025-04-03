from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from email_fetcher import authenticate_gmail, fetch_emails
from llm_integration import generate_email_response_gemini
from database import init_db, insert_email

def send_slack_message(message, channel="C08L111TK1D"):
    """
    Sends a message to a specified Slack channel.
    :param message: The text message to send.
    :param channel: The Slack channel ID.
    :return: Response from Slack API.
    """
    client = WebClient(token='xoxb-8698313086771-8698027728964-MLgSg2KdE95DPQzdW5VkxRXD')
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print(f"Slack message sent to {channel}: {message}")
        return response
    except SlackApiError as e:
        print(f"Error sending Slack message: {e.response['error']}")
        return None

def schedule_calendar_event(event_details):
    """
    Placeholder for scheduling a calendar event.
    :param event_details: Dictionary with event title and date.
    """
    print(f"Scheduling event: {event_details}")

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
        
        # Forward all emails to Slack
        send_slack_message(f"New email received: {email.get('subject')}\n{email.get('snippet')}")
        
        # If the email mentions a meeting, schedule a calendar event
        if "meeting" in email.get('snippet', '').lower():
            schedule_calendar_event({"title": email.get('subject'), "date": "2025-04-05"})
    
    print("Processing complete. All emails sent to Slack.")

if __name__ == '__main__':
    main()
