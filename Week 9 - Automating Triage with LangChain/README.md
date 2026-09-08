# Week 9 - Automating Triage with LangChain

## Objective

Learn how LangChain chains and plain Python business rules combine into a working
triage system: the chain handles the language, and Python makes every decision.

This week is a course project, so the file names come from the assignment
instead of the `_N_` prefix used in earlier weeks.

## What I built

1. **Shipment Exception Desk** - a triage desk for a logistics company. It
   classifies an exception report, calculates compensation from policy, and
   either drafts the customer email or escalates to a manager, all in a browser.

## Before running

Create `.env` in this Week 9 folder from `.env.example` and add your Groq key.
It is the same `GROQ_API_KEY` used in the earlier Groq weeks.

The assignment sets the project up with `pip` and a virtual environment. This
week uses `uv` instead, to match the rest of the repository.

## Run a project

Open this Week 9 folder in PowerShell.

### 1. Shipment Exception Desk

```powershell
Push-Location "01 - Shipment Exception Desk"
uv sync

uv run python check_setup.py
uv run python test_tools.py
uv run python triage_check.py
uv run python app.py
Pop-Location
```

Run them in that order. Each one only makes sense once the previous one passes.
See the project README for the compensation policy and the terminal runner.
