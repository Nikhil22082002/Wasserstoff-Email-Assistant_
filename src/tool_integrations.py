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
import dateparser

CHANNEL_ID = 'C08LU6MHC20'  # Slack channel ID
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar']

# agin authenticate the gmail
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
#this fucntion to fetch the mails from the gamil
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

# in this function at which channel slack message sent details
def send_slack_message(message, channel=CHANNEL_ID):
    client = WebClient(token=SLACK_token)
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print(f"✅ Slack message sent to {channel}: {message}")
        return response
    except SlackApiError as e:
        print(f"⚠️ Error sending Slack message: {e.response['error']}")
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



#extract the date and time from the mail in all the possible formate
def extract_date_and_time_from_email(snippet):
    if not snippet:
        return None

    # Look for common date + time phrases in the text
    patterns = [
        r'\b\d{1,2}(st|nd|rd|th)?\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s+(at\s+)?\d{1,2}:\d{2}\s*(AM|PM|am|pm)?',
        r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+(at\s+)?\d{1,2}:\d{2}\s*(AM|PM|am|pm)?',
        r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+(at\s+)?\d{1,2}:\d{2}\s*(AM|PM|am|pm)?',
        r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+\d{1,2}(st|nd|rd|th)?\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s+(at\s+)?\d{1,2}:\d{2}\s*(AM|PM|am|pm)?'
    ]

    for pattern in patterns:
        match = re.search(pattern, snippet, re.IGNORECASE)
        if match:
            date_time_str = match.group()
            parsed = dateparser.parse(date_time_str, settings={'PREFER_DATES_FROM': 'future'})
            if parsed:
                return parsed.strftime('%Y-%m-%d'), parsed.strftime('%H:%M:%S')  # 24-hour format

    # Fallback if no match
    fallback = dateparser.parse(snippet, settings={'PREFER_DATES_FROM': 'future'})
    if fallback:
        return fallback.strftime('%Y-%m-%d'), fallback.strftime('%H:%M:%S')  # 24-hour format

    return None



# in this function check in the mail any relate to meeting  

def is_meeting_related(snippet):
    meeting_keywords = ["meeting", "schedule", "appointment", "on", "tomorrow", "friday", "meeting on"]
    return any(keyword in snippet.lower() for keyword in meeting_keywords)
