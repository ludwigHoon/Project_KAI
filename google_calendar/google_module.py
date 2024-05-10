# Self developed Google Gmail and Calender APIs
from datetime import datetime, time
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly"]
        
TOKEN_FILE = "token.json"
CRED_FILE = "credentials.json"

class Google_api:

    def __init__(self) -> None:
        self._creds = None
        self._calendar_service = None

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
                os.remove(TOKEN_FILE)
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
            except HttpError as error:
                print(f"An error occurred: {error}")
        return self._calendar_service
    
    def Get_today_events(self) :
        """_summary_

        Returns:
            Google Events list: See  https://developers.google.com/calendar/api/v3/reference/events/list
        """        
        self.Check_auth()
        if not self._calendar_service:
            self.Get_Calender()
        
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        end_of_day = datetime.combine(datetime.now(), time.max).isoformat() + "Z"
        
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
    
        
#sample usage:

# a = Google_api()
# a.Get_Calender()
# events_result = a.Get_today_events()

# print(events_result)
# events = events_result.get("items", [])
# for event in events:
#     start = event["start"].get("dateTime", event["start"].get("date"))
#     print(start, event["summary"])
