from datetime import datetime as dt
import re

class Processed_Email:
    def __init__(self, sql_email:dict) -> None:
        self.date:int = sql_email.get("date",-1)
        self.docid:int = sql_email.get("docid",-1)
        self.subject:str = sql_email.get("c1subject","")
        self.body:str = sql_email.get("c0body","")
        self.attachments:str = sql_email.get("c2attachmentNames","")
        self.auther:str = sql_email.get("c3author","")
        self.recipients:str = sql_email.get("c4recipients","")
        self.datetime:str = sql_email.get("Datetime","")
        self.thunderlink:str = sql_email.get("ThunderLink","")
        self.folderId:int = sql_email.get("folderID",-1)
        self.messageKey:int = sql_email.get("messageKey",-1)
        
    def sanitize_text(self,text)-> str:
        # Remove newline and tab characters
        text = re.sub(r'[\n\t]', ' ', text)
        # Remove other non-printable characters (adjust the regex pattern as needed)
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        # normalize or clean up the text further as needed
        text = text.strip()
        return text

    def get_content(self) ->str:
        content = self.subject +" : " + self.body
        return self.sanitize_text(content)
    
    def get_meta(self)->dict:
        # Define a dictionary with key-value pairs
        meta_dict = {
            'date': self.date,
            'doc_id':self.docid,
            'attachements': self.attachments,
            'auther': self.auther,
            'recipients': self.recipients,
            'datetime' : self.datetime,
            'thunderlink':self.thunderlink,
            'folderId':self.folderId,
            'messageKey':self.messageKey,
            'subject': "[Email] " + self.subject
        }
        return meta_dict
    
    
class Processed_event:
    def __init__(self, sql_event:dict) -> None:
        self.doc_id:str = sql_event.get("cal_id","")
        self.start_time_micro:int = sql_event.get("event_start",-1)
        self.end_time_micro:int = sql_event.get("event_end",-1)
        self.start_time:dt = self.convert_ms_to_datetime(self.start_time_micro)
        self.end_time:dt = self.convert_ms_to_datetime(self.end_time_micro)
        self.event_name:str = self.sanitize_text(sql_event.get("title",""))
    
    def convert_ms_to_datetime(self,timestamp_microseconds:int):
        timestamp_seconds = timestamp_microseconds / 1_000_000

        # Create a datetime object
        dt_object = dt.fromtimestamp(timestamp_seconds)
        return dt_object
    
    def sanitize_text(self,text)-> str:
        # Remove newline and tab characters
        text = re.sub(r'[\n\t]', ' ', text)
        # Remove other non-printable characters (adjust the regex pattern as needed)
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        # normalize or clean up the text further as needed
        text = text.strip()
        return text

    def get_content(self) ->str:
        return self.event_name
    
    def get_meta(self)->dict:
        # Define a dictionary with key-value pairs
        meta_dict = {
            'doc_id':self.doc_id,
            'start_time_micro': self.start_time_micro,
            'end_time_micro':self.end_time_micro,
            'start_time': self.start_time.strftime("%Y-%m-%d, %H:%M"),
            'end_time': self.end_time.strftime("%Y-%m-%d, %H:%M"),
            'subject': "[Calendar] "+self.start_time.strftime("%Y-%m-%d, %H:%M") + " " + self.event_name,
            'thunderlink':""
        }
        return meta_dict
    
