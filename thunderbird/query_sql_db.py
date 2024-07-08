import sqlite3
import datetime 
import os

from email.header import decode_header

from thunderbird.tb_chroma_classes import Processed_Email, Processed_event

def get_profiles_path():
    # Get the current username
    username = os.getlogin()

    # Construct the folder path
    folder_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Thunderbird\\Profiles"
    return folder_path

def get_email_path():
    email_sql_list = []
    
    # Construct the folder path
    folder_path = get_profiles_path()

    # List all directories in the profile path
    profile_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Check if cache.sqlite exists in each profile
    for profile in profile_folders:
        full_path = os.path.join(folder_path, profile, "global-messages-db.sqlite")
        if os.path.exists(full_path):
            email_sql_list.append(full_path)
    
    return email_sql_list

def get_calender_path():
    calender_sql_list = []
    
    # Construct the folder path
    folder_path = get_profiles_path()

    # List all directories in the profile path
    profile_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Check if cache.sqlite exists in each profile
    for profile in profile_folders:
        full_path = os.path.join(folder_path, profile, "calendar-data", "cache.sqlite")
        if os.path.exists(full_path):
            calender_sql_list.append(full_path)
    
    return calender_sql_list


# Function to fetch unread emails from Thunderbird
def fetch_unread_emails(email_db:str):
    # Connect to Thunderbird's SQLite database
    # conn = sqlite3.connect('/path/to/thunderbird/profile/global-messages-db.sqlite')
    conn = sqlite3.connect(email_db)
    cursor = conn.cursor()
        
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
    
    # Get column names from the cursor
    columns = [column[0] for column in cursor.description]

    # Store results in a list of dictionaries
    emails_dict = [dict(zip(columns, row)) for row in emails]

    conn.close()

    return emails_dict

# Function to fetch today's calendar events from Thunderbird
def fetch_calendar_events(calendar_db:str):
    # Connect to Thunderbird's SQLite database for calendar events
    conn = sqlite3.connect(calendar_db)
    cursor = conn.cursor()

    # Get today's date
    now = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.min.time())
    # Calculate 24 hours ago
    twenty_four_hours_next = now + datetime.timedelta(hours=24)
    # Convert datetime to microseconds since epoch
    timestamp_micro_now = int(now.timestamp() * 1000000)
    timestamp_micro = int(twenty_four_hours_next.timestamp() * 1000000)
    SQL_email ="""SELECT 
    cal_id,
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
    
    # Get column names from the cursor
    columns = [column[0] for column in cursor.description]
    print(columns)
    # Store results in a list of dictionaries
    events_dict = [dict(zip(columns, row)) for row in events]

    conn.close()

    return events_dict

def convert_ms_to_datetime(timestamp_microseconds:int):
    timestamp_seconds = timestamp_microseconds / 1_000_000

    # Create a datetime object
    dt_object = datetime.fromtimestamp(timestamp_seconds)
    return dt_object

# Main function to fetch and process emails received 24hrs ago
def get_emails_obj()-> list:
    list_of_Processed_Email_objs =[]
    email_db_list = get_email_path()
    for email_db in email_db_list:
        unread_emails = fetch_unread_emails(email_db)
        for email in unread_emails:
            list_of_Processed_Email_objs.append(Processed_Email(email))
    return list_of_Processed_Email_objs

def get_calander_obj()->list:
    list_of_Processed_event_objs =[]
    calender_db_list = get_calender_path()
    for calender_db in calender_db_list:     
        today_events = fetch_calendar_events(calender_db)
        for event in today_events:
            list_of_Processed_event_objs.append(Processed_event(event))
    return list_of_Processed_event_objs

