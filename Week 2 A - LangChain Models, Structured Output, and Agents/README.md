# Week 2 A - LangChain Models, Structured Output, and Agents

## Objective

Learn
How LangChain allows us to call multiple different models from different providers through a common wrapper.
Structure the output in a Predefined format making the data more Serializable.
Finally
How Agents agents work and creating agents that can use tools

## Projects

1. **Calling Models with LangChain** — Compare Gemini and Groq, initialize provider-neutral models, and make manual tool calls.
2. **Structured Outputs** — Turn model responses into validated Pydantic objects, including nested data.
3. **Working with Agents** — Let LangChain manage the model-to-tool-to-model loop for inventory questions.

## Setup

This week's scripts load API keys from the repository-root `.env` file. Copy `.env.example` to `.env`, then add your keys:

```env
GOOGLE_API_KEY=your_google_ai_studio_key_here
GROQ_API_KEY=your_groq_api_key_here
```

## Run a project

Open this Week 2 A folder in PowerShell. Run one complete block at a time;
`Push-Location` enters that project and `Pop-Location` returns here afterward.

### 1. Calling Models with LangChain

```powershell
Push-Location "01 - Calling Models with LangChain"
uv sync

uv run python _1_gemini_and_groq.py
uv run python _2_init_chat_model.py
uv run python _3_model_with_a_tool.py
uv run python _4_model_with_structured_messages.py
Pop-Location
```

### 2. Structured Outputs

```powershell
Push-Location "02 - Structured Outputs"
uv sync

uv run python _1_pydantic_output.py
Pop-Location
```

`pokemon_helpers.py` is a helper module imported by the main script, so you do
not run it directly.

### 3. Working with Agents

```powershell
Push-Location "03 - Working with Agents"
uv sync

uv run python _1_basic_agent.py
uv run python _2_agent_with_multiple_tools.py
Pop-Location
```
