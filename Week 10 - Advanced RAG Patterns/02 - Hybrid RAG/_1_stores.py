# What this file does: provides the vector store and the keyword index, built over the same chunks.
"""Shared configuration for the local embedding model, Chroma, and BM25."""

import re
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi


# Keep the saved database beside this code, regardless of the terminal's current folder.
# The source PDFs live in the shared Week 10 docs folder, one level up.
PROJECT_DIRECTORY = Path(__file__).parent
DOCS_DIRECTORY = PROJECT_DIRECTORY.parent / "docs" / "products"
DATABASE_DIRECTORY = PROJECT_DIRECTORY / "chroma_db"
COLLECTION_NAME = "products"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedder() -> HuggingFaceEmbeddings:
    """Load the same free local model used when the index was created."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def open_database() -> Chroma:
    """Open the existing Chroma database without embedding the documents again."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(DATABASE_DIRECTORY),
        embedding_function=get_embedder(),
    )


def load_chunks(database: Chroma) -> list[Document]:
    """Read every stored chunk back out, so BM25 indexes exactly what Chroma holds."""
    stored = database.get()
    return [
        Document(page_content=text, metadata=metadata)
        for text, metadata in zip(stored["documents"], stored["metadatas"])
    ]


def tokenize(text: str) -> list[str]:
    """Split text into lowercase words. Hyphens stay, so 'E-922' is one token."""
    return re.findall(r"\b[\w-]+\b", text.lower())


def build_keyword_index(chunks: list[Document]) -> BM25Okapi:
    """Build the BM25 index over the same chunks the vector store holds."""
    return BM25Okapi([tokenize(chunk.page_content) for chunk in chunks])


def keyword_search(
    index: BM25Okapi, chunks: list[Document], query: str, k: int
) -> list[Document]:
    """Return the top k chunks by BM25 score, skipping chunks that match nothing."""
    scores = index.get_scores(tokenize(query))
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [chunks[i] for i in ranked[:k] if scores[i] > 0]
