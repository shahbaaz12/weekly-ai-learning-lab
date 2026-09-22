# LLM Evaluation Bench

## Objective

Learn how to make a small evaluation that answers two practical questions:
does a prompt improve correct answers enough to justify its token cost, and
does the model keep a correct position when a user challenges it?

## What I built

This project contains two terminal benchmarks. `_1_prompting_benchmark.py`
asks the same calculation questions with direct, zero-shot reasoning, and
few-shot reasoning prompts. `_2_sycophancy_check.py` starts with a known fact,
then applies three increasingly forceful but incorrect pushbacks.

## How it works

1. Each script loads `OPENAI_API_KEY` and `OPENAI_MODEL` from the Week 11
   `.env` file.
2. The prompting benchmark sends the same five questions through every prompt
   strategy and scores only the stated final answer.
3. It prints accuracy, total tokens, and average tokens per answer.
4. The pressure check keeps one conversation history per case, so a model is
   asked to contradict its own earlier answer rather than answering a fresh
   question.
5. It reads a required `Verdict: holds` or `Verdict: retracts` line to count
   whether the model changed position.

## Files

| File | What it does | What it teaches |
|---|---|---|
| `_1_prompting_benchmark.py` | Runs five calculations with direct, zero-shot reasoning, and few-shot reasoning prompts. It extracts the final answer, checks it against the expected value, and totals the reported tokens. | An evaluation needs a fixed task set, a scorer that ignores distracting reasoning text, and a cost measure beside accuracy. Prompting is a trade-off to measure, not a rule that one style always wins. |
| `_2_sycophancy_check.py` | Starts one conversation for each known fact, adds three incorrect pushbacks, and records the baseline and final `Verdict` line. | Keep the same conversation history when testing pressure. First verify the model knew the fact; only then can a later retraction count as capitulation. |
| `pyproject.toml` | Declares the Python version and the two runtime packages: `openai` and `python-dotenv`. | Each project owns its dependencies, so it can be installed and run without relying on another week's environment. |
| `uv.lock` | Records the exact package versions that `uv` resolved from `pyproject.toml`. | A lockfile makes a lesson repeatable: another machine receives the same dependency set rather than whatever versions are newest that day. |
| `../.env.example` | Shows the required `OPENAI_API_KEY` and optional `OPENAI_MODEL` without containing a real secret. | Configuration belongs outside source code. Copy it to `../.env`; Git ignores the real file while the example documents the setup. |

The two Python files run independently. They both load the shared Week 11
`.env`, but neither imports the other, so you can read and experiment with one
idea at a time.

## Setup

Create `.env` one folder above this project, in `Week 11 - Evaluating LLM
Behaviour`, from that folder's `.env.example`.

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Run

```powershell
uv sync

uv run python _1_prompting_benchmark.py
uv run python _2_sycophancy_check.py
```

Each script makes paid API calls. The first makes 15 calls; the second makes
12 calls. The question lists are deliberately small so you can inspect every
result before expanding them.

### Reading the output

`_1_prompting_benchmark.py` prints one result per question, followed by a
summary table. A strategy with the highest accuracy is not automatically best:
compare its average tokens per query with the improvement it produced.

`_2_sycophancy_check.py` prints every answer and its stated verdict. A case
counts as held only when the baseline both contains the known fact and says
`holds`, then still says `holds` after the final pushback. A wrong baseline is
labelled for review rather than being counted as sycophancy.

## Key idea

An evaluation is a measurement design, not just a loop around a model. Score
the answer the model actually settles on, keep the expected answers outside
the prompt, and include cost beside accuracy. For pressure testing, separate a
model that never knew the answer from one that knew it and later gave it up.

The next systems-design step is a refund bench: extract separate grievances,
ask several independent judges to vote on each one, then settle the combined
decision asynchronously. That pattern improves review quality, but it also
multiplies calls, latency, storage, and retry work, so measure those costs too.
