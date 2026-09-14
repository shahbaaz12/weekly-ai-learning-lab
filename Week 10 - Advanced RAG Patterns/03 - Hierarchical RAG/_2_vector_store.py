# What this file does: provides one shared embedding model and opens the two saved Chroma collections.
"""Shared configuration for the local embedding model and the two-level database."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Keep the saved database beside this code, regardless of the terminal's current folder.
PROJECT_DIRECTORY = Path(__file__).parent
DATABASE_DIRECTORY = PROJECT_DIRECTORY / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Two collections in one database: one for specifics, one for overviews.
DETAIL_COLLECTION = "detail_documents"
SUMMARY_COLLECTION = "summary_documents"


def get_embedder() -> HuggingFaceEmbeddings:
    """Load the same free local model used when the index was created."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def open_collection(name: str) -> Chroma:
    """Open one existing collection without embedding the documents again."""
    return Chroma(
        collection_name=name,
        persist_directory=str(DATABASE_DIRECTORY),
        embedding_function=get_embedder(),
    )
