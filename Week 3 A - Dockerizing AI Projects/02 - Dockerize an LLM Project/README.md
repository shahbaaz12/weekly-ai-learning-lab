# ScalerGPT

## Objective

Dockerize a small RAG application. Docker Compose starts two services:

- `app` — FastAPI application using OpenAI
- `chroma` — vector database that stores the note embeddings

## Setup

```powershell
Copy-Item .env.example .env
```

Add your OpenAI key to `.env`.

## Build, index, and ask

```powershell
docker compose up -d --build
docker compose exec app python ingest.py
```

Ask a question with the Swagger page at `http://localhost:8000/docs`, or run:

```powershell
curl.exe -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"query\":\"What is RAG?\"}"
```

The Chroma data is stored in the `chroma_data` volume, so it remains after
`docker compose down`.

## Cleanup

```powershell
docker compose down
```

Use `docker compose down -v` to remove the saved Chroma data too.
