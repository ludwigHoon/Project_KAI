from qdrant_client import QdrantClient

from settings import all_settings

settings = all_settings()
client = QdrantClient(path = settings["persist_path"])
