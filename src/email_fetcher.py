import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import GMAIL_CREDENTIALS_FILE, GMAIL_TOKEN_FILE, GMAIL_SCOPES

def authenticate_gmail():
    creds = None
    # Token file stores the user's access and refresh tokens.
    if os.path.exists(GMAIL_TOKEN_FILE):
        with open(GMAIL_TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(GMAIL_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_emails(service, query="is:unread"):
    # Fetch a list of emails matching the query
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    email_data = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        email_data.append(parse_email(msg_data))
    return email_data

def parse_email(msg_data):
    # Extract basic email fields
    headers = msg_data.get('payload', {}).get('headers', [])
    email_info = {}
    for header in headers:
        name = header.get('name')
        if name in ['From', 'To', 'Subject', 'Date']:
            email_info[name.lower()] = header.get('value')
    email_info['snippet'] = msg_data.get('snippet', '')
    return email_info

if __name__ == '__main__':
    service = authenticate_gmail()
    emails = fetch_emails(service)
    for email in emails:
        print(email)
