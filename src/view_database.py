import sqlite3
from tabulate import tabulate

# Connect to the SQLite database
conn = sqlite3.connect("emails.db")
cursor = conn.cursor()

# Fetch all stored emails
cursor.execute("SELECT * FROM emails")
rows = cursor.fetchall()

# Get column names
columns = [description[0] for description in cursor.description]

# Print data as a table
if rows:
    print(tabulate(rows, headers=columns, tablefmt="grid"))
else:
    print("No data found in the emails table.")

# Close the connection
conn.close()
