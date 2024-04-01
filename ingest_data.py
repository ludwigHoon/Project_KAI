from settings import all_settings
from vector_db import client


def preprocess_data(data_type, location):
    # Implement your data preprocessing logic here
    data = None
    return(data)


def ingest_data():
    settings = all_settings()
    for source in settings["data_sources"]:
        data = preprocess_data(source["type"], source["path"])
        client.add(
            collection_name=data["collection"], documents=data["documents"], metadata=data["metadata"], ids=data["ids"]
        )
    print("Data ingestion complete")

