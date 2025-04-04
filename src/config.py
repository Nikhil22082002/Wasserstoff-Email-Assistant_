# Configuration file for API keys and settings

# Gmail API credentials
GMAIL_CREDENTIALS_FILE = 'credentials.json'
GMAIL_TOKEN_FILE = 'token.json'
GMAIL_SCOPES = ['https://mail.google.com/']

# OpenAI API Key
GEMINI_API_KEY = "AIzaSyCPax3AOqtloAcNHL0YNncG_qLMSfGwEvY"  # Replace this with your api key
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=AIzaSyCPax3AOqtloAcNHL0YNncG_qLMSfGwEvY"  # dont need to repalce it if you used gemini-1.5-pro model.  Make sure you have the key in there.


# Slack API key (if integrating)
SLACK_token = 'xoxb-8698313086771-8698027728964-MLgSg2KdE95DPQzdW5VkxRXD'
channel="C08LU6MHC20"
# Calendar API settings could go here as well
#till now not work on there
# Database configuration (using SQLite for simplicity)
DATABASE_FILE = 'emails.db'
