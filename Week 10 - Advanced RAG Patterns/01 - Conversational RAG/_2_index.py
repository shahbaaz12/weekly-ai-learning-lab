# What this file does: reads the fable PDFs, chunks them, embeds them, and saves them in Chroma.
"""Offline RAG stage: PDF pages -> chunks -> embeddings -> saved database."""

import shutil

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from _1_vector_store import COLLECTION_NAME, DATABASE_DIRECTORY, DOCS_DIRECTORY, get_embedder


def load_pages() -> list[Document]:
    """Turn every page of every PDF in docs/ into one Document with its source."""
    pages = []

    for pdf_path in sorted(DOCS_DIRECTORY.glob("*.pdf")):
        for page_number, page in enumerate(PdfReader(pdf_path).pages, start=1):
            pages.append(
                Document(
                    page_content=page.extract_text(),
                    metadata={"source": pdf_path.name, "page": page_number},
                )
            )

    return pages


def main() -> None:
    pages = load_pages()

    # Small chunks keep each fable's moments separate, so a follow-up question
    # about one character lands on the right passage.
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=40)
    chunks = splitter.split_documents(pages)

    # Rebuilding replaces the generated local index, so repeated runs do not
    # duplicate the same source documents.
    if DATABASE_DIRECTORY.exists():
        shutil.rmtree(DATABASE_DIRECTORY)

    Chroma.from_documents(
        documents=chunks,
        embedding=get_embedder(),
        collection_name=COLLECTION_NAME,
        persist_directory=str(DATABASE_DIRECTORY),
    )

    print(f"PDF pages read: {len(pages)}")
    print(f"Indexed {len(chunks)} chunks in: {DATABASE_DIRECTORY}")


if __name__ == "__main__":
    main()
