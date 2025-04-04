Project Overview
This project automates the process of managing and responding to emails, forwarding important messages to Slack, and scheduling calendar events based on the content of the emails. The main components include integration with Gmail, Slack, and Google Calendar APIs, with additional functionality to extract dates and times from email content and schedule meetings accordingly.


Key Features:
   
   Email Parsing: Fetches unread emails from Gmail, processes the subject, sender, and snippet.
   
   Slack Integration: Sends notifications to Slack with email details (subject, sender, snippet).
   
   Google Calendar Integration: Schedules calendar events based on extracted dates/times from emails.
   
   Date Parsing: Uses dateparser to extract date/time from email snippets and schedule events accordingly.

Data Flow
   Inbox (Gmail API): The system first retrieves unread emails using the Gmail API.

   Processing Layer: The email content is analyzed for important information like dates, subjects, and senders.

   LLM (Date Parser & Logic): The LLM (Date Parser) processes the email's snippet to extract date and time. If a date is present, it is used to schedule a calendar event.

   Slack Notification: Important email details are sent to Slack via the Slack API to notify the user.

   Google Calendar: A calendar event is created based on extracted date/time using the Google Calendar API.

Requirements
   
   Python 3.x
   Gmail API
   Slack API
   Google Calendar API
   Required Python Libraries (listed in requirements.txt)

Setting Up API Credentials

Gmail API
   Go to the Google Developers Console.

   Create a new project.

   Enable the Gmail API for the project.

   Go to APIs & Services > Credentials.

   Create OAuth 2.0 Client IDs credentials and download the JSON file (credentials.json).

   Place the credentials.json file in your project directory.

Google Calendar API
   Go to the Google Developers Console.

   In the same project as above, enable the Google Calendar API.

   Use the same credentials (credentials.json) for both Gmail and Calendar APIs.

   No additional steps are needed as long as the scopes for both APIs are defined correctly (SCOPES in the code).

Slack API
   Go to Slack API.

   Create a new Slack App.

   Add the chat:write permission under OAuth & Permissions.

   Install the app to your workspace.

   Copy the Bot User OAuth Token and save it as SLACK_token in your config.py file.

   Storing and Using Tokens
   The first time you run the project, it will prompt you to authenticate the Gmail/Calendar API using OAuth. It will create a token.json file in your project directory to store your access tokens.

   The Slack token is stored in config.py and is used to send messages to Slack.   

Installation
Clone the Repository 
   
   ## git clone https://your-repository-url.git
   cd your-repository-name

Install the required libraries:

   pip install -r requirements.txt
Set Up Configuration
   
   Place your credentials.json (from Gmail and Google Calendar) in the root directory of the project.

   Add your Slack token to the config.py file:

