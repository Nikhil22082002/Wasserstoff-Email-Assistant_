import os
import dateparser
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from config import SLACK_token
# Constants for Slack and Google API credentials

CHANNEL_ID = 'C08LU6MHC20'  # Change to your desired Slack channel ID
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar']

# Authenticate with Gmail API
def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# Fetch unread emails from Gmail
def fetch_emails(service, query="is:unread"):
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    emails = []
    if not messages:
        print("No new messages.")
    else:
        for message in messages[:5]:  # Limit to 5 emails
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = {
                'subject': '',
                'snippet': '',
                'from': '',
            }
            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                if header['name'] == 'From':
                    email_data['from'] = header['value']
            email_data['snippet'] = msg['snippet']
            emails.append(email_data)
    return emails

# Send Slack message
def send_slack_message(message, channel=CHANNEL_ID):
    client = WebClient(token=SLACK_token)
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print(f"✅ Slack message sent to {channel}: {message}")
        return response
    except SlackApiError as e:
        print(f"⚠️ Error sending Slack message: {e.response['error']}")
        return None

# Forward email to Slack
def forward_email_to_slack(email):
    """
    Forwards important emails to Slack.
    :param email: Dictionary containing email details (subject, sender, snippet).
    """
    subject = email.get('subject', 'No Subject')
    sender = email.get('from', 'Unknown Sender')
    snippet = email.get('snippet', 'No Content')
    
    message = (f"*Important Email Alert!*\n"
               f"From: {sender}\n"
               f"Subject: {subject}\n"
               f"Snippet: {snippet}")
    
    send_slack_message(message)

# Authenticate with Google Calendar API
def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = authenticate_gmail()  # Use Gmail authentication for simplicity
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

# Schedule a calendar event
def schedule_calendar_event(event_details):
    service = authenticate_google_calendar()
    event = {
        'summary': event_details['title'],
        'location': 'Virtual',
        'start': {
            'dateTime': event_details['date'] + "T09:00:00",  # Adjust the time if needed
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': event_details['date'] + "T10:00:00",  # Adjust the time if needed
            'timeZone': 'Asia/Kolkata',
        },
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Event created: {created_event.get('htmlLink')}")


def handle_email_for_event(email):
    """
    Process email content and schedule a meeting based on the details.
    """
    email_snippet = email.get('snippet', '')
    date, time = extract_date_and_time_from_email(email_snippet)

    # Example: Create event with extracted date and time
    event_details = {
        'title': f"Meeting with {email['from']}",
        'date': date
    }
    schedule_calendar_event(event_details, start_time=time, end_time="10:00:00")
# Extract date from email (Optional: you can improve this to parse dates dynamically from the email content)
def extract_date_from_email(email_snippet):
    parsed_date = dateparser.parse(email_snippet)
    if parsed_date:
        return parsed_date.strftime("%Y-%m-%d")
    return "No data avi"  # Default date if no date is found


def extract_date_and_time_from_email(email_snippet):
    parsed_date = dateparser.parse(email_snippet)
    if parsed_date:
        return parsed_date.strftime("%Y-%m-%d"), parsed_date.strftime("%H:%M:%S")
    return "No data available", "09:00:00"  # Default date and time if not found

def is_meeting_related(snippet):
    meeting_keywords = ["meeting", "schedule", "appointment", "on", "tomorrow", "friday", "meeting on"]
    return any(keyword in snippet.lower() for keyword in meeting_keywords)

