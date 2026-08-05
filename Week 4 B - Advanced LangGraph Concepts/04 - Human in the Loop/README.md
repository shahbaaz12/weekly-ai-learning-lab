# Human in the Loop

## Objective

Build a graph that pauses when it needs a person to make a decision.

## Run

```powershell
uv sync
uv run python _1_human_in_the_loop.py
```

## Key idea

`interrupt` pauses the graph and keeps its state safe. `Command(resume=...)`
starts the graph again with the human answer. The example resumes automatically
with `Yes, approved.` so that you can run it from start to finish.
