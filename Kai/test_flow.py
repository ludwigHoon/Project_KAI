# Get some data

import wikipedia
from ingest_data import add_chunk_text_to_db_with_meta
from setup import reset_application

reset_application()

amd_query = wikipedia.search("AMD")
page_data = []

page_metadata = []
for page in amd_query:
    page_datum = wikipedia.page(page, auto_suggest = False)
    page_metadata.append({"url": page_datum.url})
    page_data.append(
            f'# Summary:\n{wikipedia.summary(page, auto_suggest = False)}\n\n# Content:\n{page_datum.content}'
    )

for i in range(len(page_metadata)):
    datum = page_data[i]
    meta = page_metadata[i]
    meta["doc_id"] = f"wiki_{meta['url'].split('/')[-1]}"
    add_chunk_text_to_db_with_meta(datum, meta)


