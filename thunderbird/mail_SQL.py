import sqlite3
import datetime 
import imaplib
import email
from email.header import decode_header

# Function to fetch unread emails from Thunderbird
def fetch_unread_emails():
    # Connect to Thunderbird's SQLite database
    # conn = sqlite3.connect('/path/to/thunderbird/profile/global-messages-db.sqlite')
    conn = sqlite3.connect("C:\\Users\\YZC95\\AppData\\Roaming\\Thunderbird\\Profiles\\7wbym3ph.default-esr\\global-messages-db.sqlite")
    cursor = conn.cursor()

    # Query for unread emails
    #cursor.execute("SELECT * FROM messages WHERE unread = 1 ORDER BY date DESC LIMIT 10")
    """
    SELECT 
	messages.date,
	messagesText_content.*, 
           strftime('%Y-%m-%d, %H:%M', 
                    DATETIME(messages.date/1000000, 
                    "unixepoch", "localtime")) AS `Datetime`,
			"thunderlink://" || messages.headerMessageID AS `ThunderLink`,
           messages.folderID,
           messages.messageKey
    FROM messagesText_content
    JOIN messages ON messages.id=messagesText_content.docid
    WHERE (messagesText_content.c3author NOT LIKE "%daemon%"
    OR messagesText_content.c3author NOT LIKE "%DAEMON%")
	AND messages.date > 1719712783000000
    ORDER BY messages.date DESC
    """
        
    now = datetime.datetime.utcnow()

    # Calculate 24 hours ago
    twenty_four_hours_ago = now - datetime.timedelta(hours=24)

    # Convert datetime to microseconds since epoch
    timestamp_micro = int(twenty_four_hours_ago.timestamp() * 1000000)
    SQL_email ="""SELECT 
	messages.date,
	messagesText_content.*, 
           strftime('%Y-%m-%d, %H:%M', 
                    DATETIME(messages.date/1000000, 
                    "unixepoch", "localtime")) AS `Datetime`,
			"thunderlink://" || messages.headerMessageID AS `ThunderLink`,
           messages.folderID,
           messages.messageKey
    FROM messagesText_content
    JOIN messages ON messages.id=messagesText_content.docid
    WHERE (messagesText_content.c3author NOT LIKE "%daemon%"
    OR messagesText_content.c3author NOT LIKE "%DAEMON%")
	AND messages.date > """+str(timestamp_micro)+"""
    ORDER BY messages.date DESC
    """
    cursor.execute(SQL_email)
    # cursor.execute("select * from messages where date > "+str(timestamp_micro))
    emails = cursor.fetchall()

    conn.close()

    return emails

# Function to fetch today's calendar events from Thunderbird
def fetch_calendar_events():
    # Connect to Thunderbird's SQLite database for calendar events
    conn = sqlite3.connect("C:\\Users\\YZC95\\AppData\\Roaming\\Thunderbird\\Profiles\\7wbym3ph.default-esr\\calendar-data\\cache.sqlite")
    cursor = conn.cursor()

    # Get today's date
    now = datetime.datetime.utcnow()
    # Calculate 24 hours ago
    twenty_four_hours_next = now + datetime.timedelta(hours=24)
    # Convert datetime to microseconds since epoch
    timestamp_micro_now = int(now.timestamp() * 1000000)
    timestamp_micro = int(twenty_four_hours_next.timestamp() * 1000000)
    SQL_email ="""SELECT 
	event_start,
    event_end,
	title
    FROM cal_events
    WHERE event_start > """+str(timestamp_micro_now)+"""
	AND event_start < """+str(timestamp_micro)+"""
    ORDER BY event_start DESC
    """
    cursor.execute(SQL_email)
    events = cursor.fetchall()

    conn.close()

    return events

# Main function to fetch and print unread emails and calendar events
def main():
    unread_emails = fetch_unread_emails()
    print("Unread Emails:")
    for email in unread_emails:
        print(email)
        # print(f"Subject: {email[1]}")
        # print(f"From: {email[2]}")
        
    today_events = fetch_calendar_events()
    print("Unread Emails:")
    for evnet in today_events:
        print(evnet)
        
#messages SQL table  schema, 4th is date in microseconds
# CREATE INDEX messageLocation ON messages(folderID, messageKey);
# CREATE INDEX headerMessageID ON messages(headerMessageID);
# CREATE INDEX conversationID ON messages(conversationID);
# CREATE INDEX date ON messages(date);
# CREATE INDEX deleted ON messages(deleted);
        #timestamp_sec = email[4] / 1000000

        # Convert timestamp to datetime object
        # date_obj = datetime.datetime.utcfromtimestamp(timestamp_sec)

        # Print the date in a specific format
        # print(f"Date:{date_obj.strftime('%Y-%m-%d %H:%M:%S')}")
        # print("")

    print("\nToday's Calendar Events:")
    # calendar_events = fetch_calendar_events()
    # for event in calendar_events:
    #     print(f"Summary: {event[0]}")
    #     print(f"Start Date: {event[1]}")
    #     print(f"End Date: {event[2]}")
    #     print("")

if __name__ == "__main__":
    main()
