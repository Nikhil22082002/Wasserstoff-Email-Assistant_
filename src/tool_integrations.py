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
import re
from datetime import datetime 

CHANNEL_ID = ''  # Slack channel ID
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

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

def send_slack_message(message, channel=CHANNEL_ID):
    client = WebClient(token=SLACK_token)
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print(f"Slack message sent to {channel}: {message}")
        return response
    except SlackApiError as e:
        print(f" Error sending Slack message: {e.response['error']}")
        return None

def forward_email_to_slack(email):
    subject = email.get('subject', 'No Subject')
    sender = email.get('from', 'Unknown Sender')
    snippet = email.get('snippet', 'No Content')
    
    message = (f"*Important Email Alert!*\n"
               f"From: {sender}\n"
               f"Subject: {subject}\n"
               f"Snippet: {snippet}")
    
    send_slack_message(message)

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



#extract the date and time in all formate
def extract_datetime_from_email(email_body):
    date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+ \d{1,2},? \d{4}|\d{4}-\d{2}-\d{2})\b'
    time_pattern = r'\b(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)\b'

    date_match = re.search(date_pattern, email_body)
    time_match = re.search(time_pattern, email_body)

    print(f"Found Date: {date_match.group(0) if date_match else ' No date'}")
    print(f"Found Time: {time_match.group(0) if time_match else ' No time'}")

    if date_match:
        date_str = date_match.group(0)
        time_str = time_match.group(0).upper() if time_match else "10:00 AM" 

        date_obj = None
        time_obj = None
        #formate of dates
        for fmt in ('%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y', '%d/%m/%y', '%m/%d/%y',
                    '%B %d, %Y', '%B %d,%Y', '%b %d, %Y', '%b %d,%Y','%Y-%m-%d'):
            try:
                date_obj = datetime.strptime(date_str, fmt).date()
                break
            except ValueError:
                continue

        for fmt in ('%I:%M %p', '%H:%M', '%I:%M:%S %p', '%H:%M:%S'):
            try:
                time_obj = datetime.strptime(time_str, fmt).time()
                break
            except ValueError:
                continue

        if date_obj and time_obj:
            return datetime.combine(date_obj, time_obj)

    return None


# function to check mail is related to meeting or not
def is_meeting_related(snippet):
    meeting_keywords = ["meeting", "schedule", "appointment", "on", "tomorrow", "friday", "meeting on"]
    return any(keyword in snippet.lower() for keyword in meeting_keywords)
