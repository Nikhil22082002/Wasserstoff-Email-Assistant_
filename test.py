from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Use the Bot Token (starts with xoxb-)
slack_token = "xoxb-8698313086771-8698027728964-MLgSg2KdE95DPQzdW5VkxRXD"
client = WebClient(token=slack_token)

try:
    response = client.chat_postMessage(
        channel="C08L111TK1D",  # Use the correct channel ID
        text="Hello, Slack! This is a test message."
    )
    print("Message sent:", response["ts"])
except SlackApiError as e:
    print(f"Error sending message: {e.response['error']}")
