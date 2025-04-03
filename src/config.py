# Configuration file for API keys and settings

# Gmail API credentials
GMAIL_CREDENTIALS_FILE = 'credentials.json'
GMAIL_TOKEN_FILE = 'token.json'
GMAIL_SCOPES = ['https://mail.google.com/']

# OpenAI API Key
GEMINI_API_KEY = "AIzaSyCPax3AOqtloAcNHL0YNncG_qLMSfGwEvY"  # Replace with your actual API key
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=AIzaSyCPax3AOqtloAcNHL0YNncG_qLMSfGwEvY"  # Replace with your actual endpoint.  Make sure you have the key in there.


# Slack API key (if integrating)
SLACK_API_KEY = 'YOUR_SLACK_API_KEY'

# Calendar API settings could go here as well

# Database configuration (using SQLite for simplicity)
DATABASE_FILE = 'emails.db'
