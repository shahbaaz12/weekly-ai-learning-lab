# What this file does: builds the detail collection and the summary collection from the catalog.
"""Offline RAG stage: catalog -> two levels of documents -> two saved collections."""

import shutil

from langchain_chroma import Chroma

from _1_documents import (
    load_products,
    product_documents,
    subcategory_documents,
    variant_documents,
)
from _2_vector_store import (
    DATABASE_DIRECTORY,
    DETAIL_COLLECTION,
    SUMMARY_COLLECTION,
    get_embedder,
)


def main() -> None:
    products = load_products()

    # No chunking here. Each product, variant, or summary is already one
    # self-contained document, so splitting it would only separate facts
    # that belong together.
    detail = product_documents(products) + variant_documents(products)
    summaries = subcategory_documents(products)

    # Rebuilding replaces the generated local index, so repeated runs do not
    # duplicate the same source documents.
    if DATABASE_DIRECTORY.exists():
        shutil.rmtree(DATABASE_DIRECTORY)

    embedder = get_embedder()

    for name, documents in ((DETAIL_COLLECTION, detail), (SUMMARY_COLLECTION, summaries)):
        Chroma.from_documents(
            documents=documents,
            embedding=embedder,
            collection_name=name,
            persist_directory=str(DATABASE_DIRECTORY),
        )

    print(f"Products: {len(products)}")
    print(f"Detail collection: {len(detail)} documents (products + variants)")
    print(f"Summary collection: {len(summaries)} documents (one per subcategory)")
    print(f"Saved in: {DATABASE_DIRECTORY}")


if __name__ == "__main__":
    main()
