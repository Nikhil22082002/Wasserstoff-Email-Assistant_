import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
# from tool_integrations import send_slack_message # Removed to avoid errors.  Add back if you have it.

# Define Calendar API Scopes
CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]
# for used googel_calendar service
def get_calendar_service():
    """
    Authenticate and return Google Calendar API service.
    """
    creds = None
    # Check if token already exists
    if os.path.exists("token_calendar.pickle"):
        with open("token_calendar.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no credentials are available or the token is invalid, authenticate again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "calendar_credentials.json", CALENDAR_SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open("token_calendar.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)

# schedule meeting on google calendar and also give the link to open paticular event
def schedule_calendar_event(event_details):
    """
    Schedule an event on Google Calendar.

    :param event_details: Dictionary with:
        - 'title': Event title
        - 'start_datetime': Datetime in 'YYYY-MM-DDTHH:MM:SS' format (ISO 8601)
    """
    service = get_calendar_service()

    start_datetime_str = event_details.get("start_datetime")
    title = event_details.get("title", "Meeting")

    try:
        start = datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")
        end = start + timedelta(hours=1)

        event = {
            "summary": title,
            "start": {
                "dateTime": start.isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end.isoformat(),
                "timeZone": "Asia/Kolkata",
            },
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print(f" Event Created: {created_event.get('htmlLink')}")
        return created_event

    except ValueError as e:
        print(f" Error parsing start_datetime: {e}")
        return None

