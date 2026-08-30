# Week 8 - Building an AI Interview Coach

## Objective

Build InterviewIQ, a mock-interview coach that evaluates an answer with
rule-based tools, remembers the whole session, and runs in the browser.

This week is a course project, so the file names come from the assignment
instead of the `_N_` prefix used in earlier weeks.

## What I built

1. **InterviewIQ Coach Agent** - A tool-calling evaluator agent with session
   memory, an aggregated weakest-area report, a Gradio interface, and a bonus
   second agent that chooses the next question's category.

## Before running

Create `.env` in this Week 8 folder from `.env.example` and add your Groq key.
It is the same `GROQ_API_KEY` used in the earlier Groq weeks.

The assignment sets the project up with `pip` and a virtual environment. This
week uses `uv` instead, to match the rest of the repository.

## Run a project

Open this Week 8 folder in PowerShell.

### 1. InterviewIQ Coach Agent

```powershell
Push-Location "01 - InterviewIQ Coach Agent"
uv sync

uv run python check_setup.py
uv run python test_tools.py
uv run python memory_check.py
uv run python app.py
Pop-Location
```

Run them in that order. Each one only makes sense once the previous one passes.
See the project README for the terminal runner and the optional two-agent demo.
