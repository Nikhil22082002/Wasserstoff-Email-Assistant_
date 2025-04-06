import sqlite3
from config import DATABASE_FILE
# Function for creating the database
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            recipient TEXT,
            subject TEXT,
            date TEXT,
            snippet TEXT
        )
    ''')
    conn.commit()
    conn.close()

#insert the mails in the database with this function
def insert_email(email_info):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO emails (sender, recipient, subject, date, snippet)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        email_info.get('from', ''),
        email_info.get('to', ''),
        email_info.get('subject', ''),
        email_info.get('date', ''),
        email_info.get('snippet', '')
    ))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    sample_email = {
        'from': 'example@example.com',
        'to': 'user@example.com',
        'subject': 'Test Email',
        'date': '2025-04-01',
        'snippet': 'This is a test email snippet.'
    }
    insert_email(sample_email)
