# Configuration file for API keys and settings

# Gmail API credentials
GMAIL_CREDENTIALS_FILE = 'credentials.json'
GMAIL_TOKEN_FILE = 'token.json'
GMAIL_SCOPES = ['https://mail.google.com/']

# GEMINI API Key
GEMINI_API_KEY = "AIzaSyCPax3AOqtloAcNHL0YNncG_qLMSf"  # Replace this with your api key
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=put your api key"  # dont need to repalce it if you used gemini-1.5-pro model.  Make sure you have the key in there.

# Slack API key 
SLACK_token = 'slack api token'
channel="your channel "

# Database configuration (using SQLite for simplicity)
DATABASE_FILE = 'emails.db'
