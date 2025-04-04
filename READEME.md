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

   