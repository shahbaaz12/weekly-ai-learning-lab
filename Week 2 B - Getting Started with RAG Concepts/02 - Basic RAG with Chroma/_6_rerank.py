# What this file does: improves the vector-search order by scoring shortlisted chunks more carefully.
"""Optional improvement: rerank vector-search candidates with a cross-encoder."""

import sys

from sentence_transformers import CrossEncoder

from _2_vector_store import open_database


DEFAULT_QUESTION = "What are the rules for returning an unused item?"


def main() -> None:
    # Let you supply another question after the script name in the terminal.
    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
    database = open_database()

    # First pass: vector retrieval is fast and gets a reasonable shortlist.
    candidates = database.similarity_search(question, k=6)

    # Second pass: the cross-encoder reads the question and each chunk together.
    # It is slower, so we apply it only to the small shortlist.
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
    scores = reranker.predict([(question, chunk.page_content) for chunk in candidates])

    # Sort from most relevant to least relevant before returning the best three.
    ranked_results = sorted(
        zip(scores, candidates),
        key=lambda result: float(result[0]),
        reverse=True,
    )

    print(f"Question: {question}")
    print("\nReranked chunks (higher cross-encoder score is better):")

    for rank, (score, chunk) in enumerate(ranked_results[:3], start=1):
        print(f"\n--- Result {rank} | reranker score: {float(score):.3f} ---")
        print(chunk.page_content)


if __name__ == "__main__":
    main()
