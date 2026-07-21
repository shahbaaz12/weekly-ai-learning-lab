# What this file does: provides one shared embedding model and opens the saved Chroma database.
"""Shared configuration for the local embedding model and Chroma database."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Keep the saved database beside this code, regardless of the terminal's current folder.
PROJECT_DIRECTORY = Path(__file__).parent
DATABASE_DIRECTORY = PROJECT_DIRECTORY / "chroma_db"
COLLECTION_NAME = "company_policies"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embedder() -> HuggingFaceEmbeddings:
    """Load the same free local model used when the index was created."""
    # The indexing and querying stages must use the same embedding model.
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def open_database() -> Chroma:
    """Open the existing Chroma database without embedding the documents again."""
    # Open the persisted vectors and attach the embedder for new search queries.
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(DATABASE_DIRECTORY),
        embedding_function=get_embedder(),
    )
