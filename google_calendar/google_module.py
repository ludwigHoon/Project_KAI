# Self developed Google Gmail and Calender APIs
import base64
import datetime
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/contacts.readonly",
            "https://www.googleapis.com/auth/contacts.readonly"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        
TOKEN_FILE = SCRIPT_DIR+"/token.json"
CRED_FILE = SCRIPT_DIR+"/credentials.json"

class Google_api:

    def __init__(self) -> None:
        self._creds = None
        self._calendar_service = None
        self._people_service = None
        self._email_service = None

    def Authenticate(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        self._creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_FILE):
            self._creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                #os.remove(TOKEN_FILE)
                print("Refresh token")
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CRED_FILE, SCOPES
                )
                self._creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(TOKEN_FILE, "w") as token:
                    token.write(self._creds.to_json())
                
    def Check_auth(self):
        """Check authentiication status, if no proceed with Authenticate function
        """
        if not self._creds:
            self.Authenticate()
            
    def Get_Calender(self):
        self.Check_auth()
        if not self._calendar_service:
            try:
                self._calendar_service = build("calendar", "v3", credentials=self._creds)
                self._people_service  = build("people", "v1", credentials=self._creds)
                self._email_service = build('gmail', 'v1', credentials=self._creds)
            except HttpError as error:
                print(f"An error occurred: {error}")
    
    def Get_today_events(self) :
        """_summary_

        Returns:
            Google Events list: See  https://developers.google.com/calendar/api/v3/reference/events/list
        """        
        self.Check_auth()
        if not self._calendar_service:
            self.Get_Calender()
        
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        end_of_day = datetime.datetime.combine(datetime.datetime.now(), datetime.time.max).isoformat() + "Z"
        
        events_result = (
        self._calendar_service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=end_of_day,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
        )
        
        return events_result
    
    def Get_attendee_name(self, email:str):
        if not self._people_service:
            self.Get_Calender()
        person_details = (
            self._people_service.people().
                searchContacts(query=email, readMask="locations,metadata,names,nicknames,phoneNumbers,relations")
                .execute()
        )
        print("\ndetails: ",email,person_details)
        contacts_details = person_details.get('results')
        if(contacts_details and len(contacts_details)>=1):
            print("\n1st: ",contacts_details[0])
            return True, contacts_details[0].get('person')
        else:
            return  False, email
    
    def construct_event_metadata(self, event):
        """Contruct a single Google Event Dict to a Meta and base info

        Args:
            events_result (Google Event Dict): _description_

        Returns:
            str: event name
            str: event description
            dic: Meta data
        """

        meta = dict()
        eventName:str = ""
        note:str = ""
        
        if(event):
            #Meta constrcutions
            start = event.get("start").get("datetime.datetime", event.get("start").get("date"))
            end   = event.get("end").get("datetime.datetime", event.get("end").get("date"))
            location = event.get("location") if event.get("location") else "Not Defined"
            attendees = []
            
            for attendee in event.get("attendees"):
                #if not attendee.get('self'):
                email = attendee.get('email')
                res, details = a.Get_attendee_name(email)
                if res:
                    print(details.get("names"))
                    person = details.get("names")[0].get("displayName")  + "<"+email+">"
                    attendees.append(person)
                else:
                    attendees.append( "<"+email+">")
                    
            meta["start"] = start
            meta["end"] = end
            meta["location"] = location
            meta["attendees"] = attendees
            
            #get title and descriptiopn
            eventName = event.get("summary")
            note = event.get("description")

            
            return eventName, note, meta
        else:
            return None,None,None

    def get_unread_emails(self):
        """Get all unread email from yesterday to now
        """
        # Calculate the time range
        now = datetime.datetime.utcnow()
        yesterday = now - datetime.timedelta(days=1)
        query = f'is:unread after:{yesterday.strftime("%Y/%m/%d")} before:{now.strftime("%Y/%m/%d")}'
        
        # Get the unread emails within the specified range
        results = self._email_service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        messages_meta = []
        if not messages:
            print('No new unread messages found.')
        else:
            for message in messages:
                # msg =  self._email_service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                # headers = msg['payload']['headers']
                # subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                # parts = msg['payload']['parts']
                
                # body = ""
                # for part in parts:
                #     if part['mimeType'] == 'text/plain':
                #         body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                #         break
                
                # print(f"Subject: {subject}")
                # print(f"Body: {body}")
                
                ######## GET SNIPPET content - avoid junk info(eg css + links + footer)
                msg = self._email_service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject', 'Date']).execute()
                headers = msg['payload']['headers']
                subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                date = next(header['value'] for header in headers if header['name'] == 'Date')
                snippet = msg['snippet']
                messages_meta.append({"date":date,"subject": subject, "content":snippet})

        return messages_meta
        
#sample usage:

# a = Google_api()
# a.Get_Calender()
# events_result = a.Get_today_events()

# events = events_result.get("items", [])
# print(events)
# for event in events:
#     start = event["start"].get("datetime.datetime", event["start"].get("date"))
#     print(start, event["summary"])
#     print(event["location"])
#     print(event["attendees"])
#     # for attendee in event.get("attendees"):
#     #     if not attendee.get('self'):
#     #         res, details = a.Get_attendee_name(attendee.get('email'))
#     #         if res:
#     #             print(details)
#     name, note, meta = a.construct_event_metadata(event)
#     print(name, note, meta)
    
# msgs = a.get_unread_emails()
# print(msgs)
    
