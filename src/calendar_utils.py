from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import pickle
import os
from tool_integrations import send_slack_message
from datetime import datetime, timedelta

# Define Calendar API Scopes
CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    """
    Authenticate and return Google Calendar API service.
    """
    creds = None
    if os.path.exists("token_calendar.pickle"):
        with open("token_calendar.pickle", "rb") as token:
            creds = pickle.load(token)

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


def schedule_calendar_event(event_details):
    """
    Schedule an event on Google Calendar.
    
    :param event_details: Dictionary with event 'title' and 'date' (YYYY-MM-DD format).
    """
    service = get_calendar_service()

    event = {
        "summary": event_details["title"],
        "start": {
            "dateTime": event_details["date"] + "T10:00:00",
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": event_details["date"] + "T11:00:00",
            "timeZone": "Asia/Kolkata",
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"✅ Event Created: {event.get('htmlLink')}")
    return event
def propose_alternative_time(email):
    """
    If no specific date or time is found in the email, propose an alternative time.
    :param email: Dictionary containing email details (subject, sender, snippet).
    """
    # Define alternative times (you can make this dynamic based on your actual availability)
    current_time = datetime.now()
    available_times = [
        (current_time + timedelta(days=1)).strftime("%Y-%m-%dT09:00:00"),  # Tomorrow at 9 AM
        (current_time + timedelta(days=1)).strftime("%Y-%m-%dT14:00:00"),  # Tomorrow at 2 PM
        (current_time + timedelta(days=2)).strftime("%Y-%m-%dT10:00:00"),  # Day after tomorrow at 10 AM
    ]

    # Prepare message proposing alternative times
    subject = email.get('subject', 'No Subject')
    sender = email.get('from', 'Unknown Sender')
    message = (f"Hello {sender},\n\n"
               f"Thank you for your email regarding the meeting.\n\n"
               "Unfortunately, I couldn't find a specific date mentioned in your email. "
               "However, I am available at the following times:\n\n"
               f"1. {available_times[0]} (Tomorrow at 9 AM)\n"
               f"2. {available_times[1]} (Tomorrow at 2 PM)\n"
               f"3. {available_times[2]} (Day after tomorrow at 10 AM)\n\n"
               "Please let me know which time works best for you.\n\n"
               "Best regards,\n[Your Name]")

    # Send the email with proposed times
    send_email_reply(subject, sender, message)

    # Optionally, send a Slack message too (if required)
    send_slack_message(f"📧 Sent an alternative meeting proposal to {sender}: {message}")

def send_email_reply(subject, sender, message):
    """
    Sends a reply to the email with the proposed time options.
    :param subject: The subject of the original email.
    :param sender: The email address of the sender.
    :param message: The message body to send in the reply.
    """
    # Assuming you have an email sending function available (this is a placeholder function)
    # Replace this with your actual email sending logic
    print(f"📩 Sending reply to {sender}...\nSubject: {subject}\nMessage: {message}")
    # Uncomment this line to actually send an email using your service
    # send_email_via_gmail(subject, sender, message)