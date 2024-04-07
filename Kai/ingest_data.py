import sys

import chromadb
import tiktoken
from loguru import logger

from .setting import PERSISTANT_PATH

logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

client = chromadb.PersistentClient(path=PERSISTANT_PATH)

def add_chunk_text_to_db_with_meta(text: str, meta: dict) -> bool:
    """Add chunked text to the database with meta data
    @parameter: text : str - Text to be chunked
    @parameter: meta : dict - Meta data to be stored with the text
    """
    chunks = chunk_text(text)
    if (meta["doc_id"] is None) or (meta["doc_id"] == ""):
        logger.error("Document ID is missing")
        return(False)

    collection = client.get_or_create_collection(name="KAI", metadata={"hnsw:space": "cosine"})
    collection.upsert(
        documents = chunks,
        metadatas = [meta for i in range(len(chunks))],
        ids = [f"{meta['doc_id']}_{i}" for i in range(len(chunks))]
    )
    return(True)

def chunk_text(text: str, units: int = 256, overlap: int = 50) -> list[str]:
    """Chunk text into smaller pieces based on units and overlap
    @parameter: text : str - Text to be chunked
    @parameter: units : int - How many units per chunk (token)
    @parameter: overlap : int - How much overlap between the chunks
    @returns list[str] - List of chunks
    """
    encoding = tiktoken.encoding_for_model("gpt-4")
    encoded_tokens = encoding.encode(text, disallowed_special=())
    chunks = []

    if units > len(encoded_tokens) or units < 1:
        return([text])

    if overlap >= units:
        logger.error(
            f"Overlap value is greater than unit (Units {units}/ Overlap {overlap})"
        )
        return(None)

    i = 0
    while i < len(encoded_tokens):
        # Overlap
        start_i = i
        end_i = min(i + units, len(encoded_tokens))

        chunk_tokens = encoded_tokens[start_i:end_i]
        chunk_text = encoding.decode(chunk_tokens)

        chunks.append(chunk_text)
        i += units - overlap
    return(chunks)

