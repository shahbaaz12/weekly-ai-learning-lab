# What this file does: splits one policy document into smaller overlapping chunks for RAG.
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main() -> None:
    # Imagine this came from a page in a company policy document.
    document = """
Our return policy allows refunds within 30 days of purchase.
Items must be unused and returned with the original receipt.

Shipping is free for orders above Rs 999 across India.
Standard delivery usually takes three to five business days.

For corporate orders above 50 units, contact sales@example.com.
Our sales team can provide bulk pricing and delivery estimates.
""".strip()

    # Recursive chunking tries paragraphs, then sentences, then smaller pieces.
    # Overlap keeps nearby context when a sentence falls at a chunk boundary.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=30,
    )

    # These chunks are the smaller pieces we would embed and save in a vector database.
    chunks = splitter.split_text(document)

    print(f"Original document length: {len(document)} characters")
    print(f"Number of chunks created: {len(chunks)}")

    for number, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {number} ({len(chunk)} characters) ---")
        print(chunk)


if __name__ == "__main__":
    main()
