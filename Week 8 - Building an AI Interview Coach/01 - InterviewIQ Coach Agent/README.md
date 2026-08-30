# InterviewIQ Coach Agent

## Objective

Build a mock-interview coach that scores an answer with tools, remembers every
answer in the session, and names the candidate's weakest area in the browser.

## What I built

An evaluator agent with three rule-based tools, session memory that lasts the
whole interview, an aggregated report, a Gradio interface, and a bonus second
agent that chooses what to ask next.

## How it works

1. `interview_bank.py` holds the questions and the keywords a good answer covers.
2. The agent reads one answer and decides which tools to call.
3. `tools.py` measures filler words, STAR structure, and keyword relevance.
4. The agent turns those numbers into three short lines of feedback.
5. Every evaluated turn is saved, so the report can compare all of them.
6. `app.py` puts the whole flow in the browser.

## Files

| File | What it is |
|---|---|
| `interview_bank.py` | The questions, their category, and their expected keywords. |
| `tools.py` | The three rule-based tools. No LLM calls happen here. |
| `agent.py` | The tool-calling loop, session memory, and the aggregated report. |
| `app.py` | The Gradio interface. |
| `main.py` | Terminal runner, handy while building. |
| `check_setup.py` | One plain LLM call, to prove the key and model work. |
| `test_tools.py` | Runs the three tools directly, with no agent and no LLM. |
| `memory_check.py` | Proves the report uses the whole session, not the last turn. |
| `interviewer_agent.py` | Bonus. A second agent that picks the next category. |
| `run_multi_agent.py` | Bonus. The orchestrator loop for the two agents. |

## Setup

Create `.env` in the Week 8 folder from `.env.example`, then add your Groq key.

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

## Run

Build order. Each step only makes sense once the one above it passes.

```powershell
uv sync

uv run python check_setup.py
uv run python test_tools.py
uv run python memory_check.py
uv run python app.py
```

`main.py` runs the same interview in the terminal, and
`run_multi_agent.py` runs the optional two-agent version:

```powershell
uv run python main.py
uv run python run_multi_agent.py
```

## Two entry points to the same agent

`agent.py` exposes both:

- `InterviewCoach` is a class, so the Gradio app gives every browser session its
  own memory instead of sharing one global list.
- `run_turn`, `ask_agent`, and `ask_for_final_report` are module-level functions
  that wrap one shared coach. The course's own `memory_check.py` imports these
  names, so the project works against that script unchanged.

## Key idea

The numbers are calculated in Python and only *described* by the model.
`session_summary` finds the average and the lowest-scoring question, then hands
those facts to the model as text it must not recalculate. That is why the coach
still names the right weakest area when the most recent answer was a strong one,
which is exactly what `memory_check.py` tests.
