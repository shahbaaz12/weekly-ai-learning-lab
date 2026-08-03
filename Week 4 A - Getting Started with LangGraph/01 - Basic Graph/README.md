# Basic Graph

## Objective

Start with the smallest useful LangGraph. It has two steps and both steps update
the same state.

## Run

```powershell
uv sync
uv run python _1_basic_graph.py
```

## Key idea

`GraphState` is the information that moves through the graph. Each step adds one
to `id` and adds a message. The edges decide that step one runs before step two.

You should see a final id of `2` and three messages: the starting message and
one message from each step.
