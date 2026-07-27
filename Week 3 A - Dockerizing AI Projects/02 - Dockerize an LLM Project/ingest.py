# What this file does: reads the sample notes, splits them into paragraphs, and stores them in Chroma.

import os
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions


api_key = os.environ["OPENAI_API_KEY"]
embedder = embedding_functions.OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-small",
)
chroma = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "chroma"),
    port=int(os.getenv("CHROMA_PORT", "8000")),
)
collection = chroma.get_or_create_collection(name="notes", embedding_function=embedder)

documents = []
ids = []

for path in sorted(Path("docs").glob("*.*")):
    chunks = path.read_text(encoding="utf-8").split("\n\n")
    for number, chunk in enumerate(chunks):
        documents.append(chunk)
        ids.append(f"{path.stem}-{number}")

collection.upsert(ids=ids, documents=documents)
print(f"Indexed {len(documents)} chunks")
