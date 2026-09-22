# Week 11 - Evaluating LLM Behaviour

## Objective

Learn how to measure an LLM's answers instead of trusting a single impressive
response: compare prompting strategies, count their token cost, and check
whether a model keeps a correct answer when a user pushes back.

## What I built

1. **LLM Evaluation Bench** - two small, repeatable checks. The first compares
   direct, zero-shot reasoning, and few-shot reasoning on arithmetic questions.
   The second records whether a model holds its position through escalating
   pressure on low-stakes facts.

## Project map

| Run | What it does | What it teaches |
|---|---|---|
| `_1_prompting_benchmark.py` | Sends five calculations through three prompt styles, then reports accuracy and tokens. | Better answers are only useful when their extra token cost is worth paying. |
| `_2_sycophancy_check.py` | Pushes back three times after the model answers a known fact. | A model that changes a correct answer under pressure has a reliability problem, not a knowledge problem. |

Read the project README before running it. It explains the small scoring rules
that make each result meaningful.

## Before running

Create `.env` in this Week 11 folder from `.env.example`, then add an OpenAI
API key. `OPENAI_MODEL` defaults to `gpt-4o-mini`, a non-reasoning model, so
the different prompt shapes remain visible in the benchmark.

## Run a project

Open this Week 11 folder in PowerShell.

### 1. LLM Evaluation Bench

```powershell
Push-Location "01 - LLM Evaluation Bench"
uv sync

uv run python _1_prompting_benchmark.py
uv run python _2_sycophancy_check.py
Pop-Location
```

Run the prompting benchmark more than once. LLM output varies, so one result
is an observation, not a conclusion.
