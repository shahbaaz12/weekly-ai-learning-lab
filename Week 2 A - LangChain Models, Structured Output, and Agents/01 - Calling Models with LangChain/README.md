# Calling Models with LangChain

## Objective

Learn that LangChain gives different model providers a common chat-model interface, then see how a model can request a local tool.

## Scripts

| Script | What it demonstrates |
|---|---|
| `_1_gemini_and_groq.py` | Direct `ChatGoogleGenerativeAI` and `ChatGroq` model calls. |
| `_2_init_chat_model.py` | Provider-neutral model initialization with `init_chat_model()`. |
| `_3_model_with_a_tool.py` | A short, manual tool-call example. |
| `_4_model_with_structured_messages.py` | System, human, AI, and tool messages in a complete manual tool-call flow. |

## Requirements

- Python 3.11+
- `uv`
- `GOOGLE_API_KEY` and `GROQ_API_KEY` in the repository-root `.env` file

## Run

Run these commands from this folder:

```powershell
uv sync
uv run python _1_gemini_and_groq.py
uv run python _2_init_chat_model.py
uv run python _3_model_with_a_tool.py
uv run python _4_model_with_structured_messages.py
```

## Key idea

The first two scripts show the shared `.invoke()` interface. The final two scripts show the manual sequence behind tool calling: the model requests a tool, Python executes it, and the tool result is returned to the model.
