# DeskBuddy

## Objective

Run three services with Docker Compose:

- `agent` — OpenAI-powered chat service on port 9000
- `tools` — calculator and clock service, available only to the agent
- `redis` — stores conversation history by session ID

## Setup and run

```powershell
Copy-Item .env.example .env
```

Add your OpenAI key to `.env`, then start the stack:

```powershell
docker compose up -d --build
```

Test the agent:

```powershell
curl.exe -X POST http://localhost:9000/chat -H "Content-Type: application/json" -d "{\"session_id\":\"demo\",\"message\":\"What is 23 times 47, and what time is it?\"}"
```

Ask a follow-up with the same session ID to see Redis memory:

```powershell
curl.exe -X POST http://localhost:9000/chat -H "Content-Type: application/json" -d "{\"session_id\":\"demo\",\"message\":\"Double that result.\"}"
```

## Key idea

Only the `agent` service publishes a port. The `tools` service stays private and
is reached by the agent at `http://tools:7000` through the Docker network.

## Cleanup

```powershell
docker compose down
```

Use `docker compose down -v` to remove the Redis memory volume too.
