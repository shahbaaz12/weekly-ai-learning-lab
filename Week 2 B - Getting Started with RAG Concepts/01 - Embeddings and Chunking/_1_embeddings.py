# What this file does: compares the meanings of sentences by turning them into embeddings.
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer


def cosine_similarity(vector_a, vector_b) -> float:
    """Return a score from -1 to 1. Higher means more similar."""
    return float(dot(vector_a, vector_b) / (norm(vector_a) * norm(vector_b)))


def main() -> None:
    # This free model runs locally and turns text into 384-number vectors.
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Use one related and one unrelated sentence to make the comparison visible.
    first_sentence = "A cat is sleeping on the couch."
    similar_sentence = "A kitten is napping on the sofa."
    different_sentence = "The stock market closed higher today."

    # Encode converts a sentence into its embedding vector.
    first_vector = model.encode(first_sentence)
    similar_vector = model.encode(similar_sentence)
    different_vector = model.encode(different_sentence)

    # Higher cosine scores mean the embeddings represent more similar meanings.
    similar_score = cosine_similarity(first_vector, similar_vector)
    different_score = cosine_similarity(first_vector, different_vector)

    print(f"Embedding dimensions: {first_vector.shape}")
    print(f"First 5 values: {first_vector[:5]}")
    print()
    print(f"Sentence 1: {first_sentence}")
    print(f"Similar sentence: {similar_sentence}")
    print(f"Similarity score: {similar_score:.3f}")
    print()
    print(f"Different sentence: {different_sentence}")
    print(f"Similarity score: {different_score:.3f}")


if __name__ == "__main__":
    main()
