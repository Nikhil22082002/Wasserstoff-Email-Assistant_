from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define scopes
GMAIL_SCOPES = ["https://mail.google.com/"]
CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Load Gmail credentials
def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file("gmail_credentials.json", GMAIL_SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

# Load Google Calendar credentials
def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file("calendar_credentials.json", CALENDAR_SCOPES)
    creds = flow.run_local_server(port=0)
    return build("calendar", "v3", credentials=creds)
