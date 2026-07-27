# Week 3 A - Dockerizing AI Projects

## Objective

Learn Docker by packaging three AI projects that grow in complexity:

1. **Dockerize an ML Project** — build one FastAPI container that serves an ETA model.
2. **Dockerize an LLM Project** — run a RAG application and Chroma together with Docker Compose.
3. **Dockerize an Agentic Project** — run an agent, its tools service, and Redis with Docker Compose.

## Requirements

- Docker Desktop running
- An OpenAI API key for projects 2 and 3

Check Docker before starting:

```powershell
docker --version
docker compose version
docker run hello-world
```

## Run a project

Open this Week 3 A folder in PowerShell. Run one project at a time.

### 1. Dockerize an ML Project

```powershell
Push-Location "01 - Dockerize an ML Project"
docker build -t quickbite-eta:v1 .
docker run -d -p 8000:8000 --name quickbite-eta quickbite-eta:v1
Pop-Location
```

Open `http://localhost:8000/docs` to test the prediction API.

### 2. Dockerize an LLM Project

```powershell
Push-Location "02 - Dockerize an LLM Project"
Copy-Item .env.example .env
# Add OPENAI_API_KEY to .env.
docker compose up -d --build
docker compose exec app python ingest.py
Pop-Location
```

### 3. Dockerize an Agentic Project

```powershell
Push-Location "03 - Dockerize an Agentic Project"
Copy-Item .env.example .env
# Add OPENAI_API_KEY to .env.
docker compose up -d --build
Pop-Location
```

Each project README contains its test command and cleanup command.
