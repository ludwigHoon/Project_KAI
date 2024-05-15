# Get some data

from datetime import datetime

import wikipedia
from tqdm import tqdm

from google_calendar.google_module import Google_api

from .ingest_data import add_chunk_text_to_db_with_meta


def search_and_add_to_db(search_term: str, progress=tqdm):
    page_ids = []
    query = wikipedia.search(search_term)

    # for page in query:
    #     try:
    #         page_datum = wikipedia.page(page, auto_suggest = False)
    #         if page_datum.pageid in page_ids:
    #             continue
    #         else:
    #             page_ids.append(page_datum.pageid)
    #     except wikipedia.DisambiguationError as e:
    #         page_datum = wikipedia.page(e.options[0], auto_suggest = True)
    #         if page_datum.pageid in page_ids:
    #             continue
    #         else:
    #             page_ids.append(page_datum.pageid)

    # for page_id in progress(page_ids):
    #     page = wikipedia.page(pageid=page_id)
    #     meta = {"url": page.url, "accessed": datetime.now().isoformat()}
    #     datum = (
    #         f'# Summary:\n{page.summary}\n\n# Content:\n{page.content}')
    #     meta["doc_id"] = f"wiki_{meta['url'].split('/')[-1]}"
    #     add_chunk_text_to_db_with_meta(datum, meta)

    Google_api_services = Google_api()
    Google_api_services.Get_Calender()
    events_result = Google_api_services.Get_today_events()

    events = events_result.get("items", [])
    for event in events:
        name, note, meta = Google_api_services.construct_event_metadata(event)
        print(name, note, meta)
        meta['doc_id'] = msg['start']
        datum = (
            f'# Event name:\n{name}\n\n# Details:\n{note}')
        add_chunk_text_to_db_with_meta(datum, meta)

        
    msgs = Google_api_services.get_unread_emails()
    for msg in msgs:
        datum = (
            f'# email subject:\n{msg["subject"]}\n\n# email content:\n{msg["content"]}')
        meta = dict()
        meta['date'] = msg['date']
        meta['doc_id'] = msg['date']
        print(meta,datum)
        add_chunk_text_to_db_with_meta(datum, meta)
        
