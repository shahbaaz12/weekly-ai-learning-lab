# What this file does: creates chunks, embeds them, and saves them in the local Chroma database.
"""Offline RAG stage: chunk, embed, and save the source documents."""

import shutil

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from _1_documents import DOCUMENTS
from _2_vector_store import COLLECTION_NAME, DATABASE_DIRECTORY, get_embedder


def main() -> None:
    # A small chunk size makes the retrieval results easy to inspect in this demo.
    splitter = RecursiveCharacterTextSplitter(chunk_size=180, chunk_overlap=30)
    chunks = splitter.create_documents(DOCUMENTS)

    # Rebuilding replaces the generated local index, so repeated runs do not
    # duplicate the same source documents.
    if DATABASE_DIRECTORY.exists():
        shutil.rmtree(DATABASE_DIRECTORY)

    # Chroma creates an embedding for every chunk, then saves both the text and vectors.
    Chroma.from_documents(
        documents=chunks,
        embedding=get_embedder(),
        collection_name=COLLECTION_NAME,
        persist_directory=str(DATABASE_DIRECTORY),
    )

    print(f"Indexed {len(chunks)} chunks in: {DATABASE_DIRECTORY}")
    print("Indexing is complete. You can now retrieve from this saved database.")


if __name__ == "__main__":
    main()
