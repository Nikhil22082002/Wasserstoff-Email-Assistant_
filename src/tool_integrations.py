from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

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

def schedule_calendar_event(event_details):
    """
    Placeholder for scheduling a calendar event.
    :param event_details: Dictionary with event title and date.
    """
    print(f"Scheduling event: {event_details}")

if __name__ == '__main__':
    test_email = {
        "from": "ceo@company.com",
        "subject": "Urgent Meeting Tomorrow",
        "snippet": "We need to discuss the product launch. Please join the meeting at 10 AM."
    }
    
    forward_email_to_slack(test_email)
    schedule_calendar_event({"title": "Meeting", "date": "2025-04-02"})
