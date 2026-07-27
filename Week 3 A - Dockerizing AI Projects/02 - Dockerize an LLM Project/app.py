# What this file does: retrieves note chunks from Chroma and asks OpenAI to answer from them.

import os

import chromadb
from chromadb.utils import embedding_functions
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel


app = FastAPI(title="ScalerGPT")
api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(api_key=api_key)

embedder = embedding_functions.OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-small",
)
chroma = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "chroma"),
    port=int(os.getenv("CHROMA_PORT", "8000")),
)
collection = chroma.get_or_create_collection(name="notes", embedding_function=embedder)


class Question(BaseModel):
    query: str


@app.get("/")
def health():
    return {"status": "ScalerGPT is live", "docs_indexed": collection.count()}


@app.post("/ask")
def ask(question: Question):
    hits = collection.query(query_texts=[question.query], n_results=3)
    documents = hits["documents"][0]
    context = "\n\n---\n\n".join(documents)

    prompt = (
        "Answer using only the context below. If the answer is not in the context, "
        "say you do not know.\n\n"
        f"Context:\n{context}"
    )
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question.query},
        ],
    )

    return {"answer": response.choices[0].message.content, "sources_used": len(documents)}
