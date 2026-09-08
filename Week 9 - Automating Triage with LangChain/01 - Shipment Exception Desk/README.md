# Shipment Exception Desk

## Objective

Learn how a few LangChain chains and plain Python `if` statements become an
automated triage desk that classifies a problem, prices it, and decides whether
a human needs to see it.

## What I built

A Gradio desk for Northwind Logistics. An analyst pastes a shipment exception
report, and the app classifies it, calculates compensation from policy, then
either drafts the customer email or escalates to a manager.

## How it works

1. `classify_chain` reads the report and returns one word: delayed, damaged, lost, or unknown.
2. Plain Python routes that word to the matching compensation calculator.
3. The calculator returns a dict, because the amount decides what happens next.
4. Anything over the tier's limit, or anything unknown, is escalated.
5. `escalate_chain` writes the manager note, or `draft_email_chain` writes the customer email.
6. Every outcome is saved, so the Daily Summary can aggregate the whole day.

The chains only handle language. Every number and every decision is Python.

## Files

| File | What it is |
|---|---|
| `llm.py` | The one chat model the chains share. |
| `chains.py` | The three chains, each built as `prompt \| model \| parser`. |
| `tools.py` | The compensation policy, as three calculators. No LLM call here. |
| `pipeline.py` | The core exercise. Classify, price, route, draft. |
| `session.py` | The Daily Triage Log and the aggregated summary. |
| `app.py` | The Gradio interface. |
| `main.py` | Terminal runner, handy while building. |
| `check_setup.py` | Runs one chain, to prove the key and model work. |
| `test_tools.py` | Runs the calculators directly, with no chain and no LLM. |
| `triage_check.py` | Feeds four canned reports through and checks where each lands. |

## The compensation policy

The assignment describes "compensation per policy" but never states the policy,
so these numbers are this project's own. They all live at the top of `tools.py`.

| Category | Rule |
|---|---|
| Delayed | 2% of shipment value per day late, minimum $10, capped at 25% of value |
| Damaged | The damaged share of the value, minimum $25 |
| Lost | The full value plus a 10% service credit |

Escalation happens when compensation goes over the customer's limit, or when the
report cannot be classified at all.

| Customer tier | Escalates above |
|---|---|
| Premium | $250 |
| Standard | $500 |

Premium has the lower limit on purpose. A premium customer reaches a human
sooner, not later.

Severity comes out of the report text. `read_days_late` looks for "3 days" and
`read_damage_percent` looks for "40%", falling back to describing words such as
"minor" or "crushed".

## Setup

Create `.env` in the Week 9 folder from `.env.example`, then add your Groq key.

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
uv run python triage_check.py
uv run python app.py
```

`main.py` runs the same desk in the terminal:

```powershell
uv run python main.py
```

## Key idea

The chain classifies, and Python decides. Keeping the money and the routing out
of the prompt means the same report always produces the same payout, and a
wrong branch can be found by reading `pipeline.py` instead of re-reading a
model's answer.
