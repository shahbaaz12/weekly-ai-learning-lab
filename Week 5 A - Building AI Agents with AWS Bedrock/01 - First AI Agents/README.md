# First AI Agents

## Objective

Start with a simple agent, then see what changes when the agent has a tool.

## Before running

This project uses the AWS credentials and MODEL_ID from the Week 5 .env file.

## Run

~~~powershell
uv sync
uv run python _1_hello_world_agent.py
uv run python _2_langgraph_agent_with_tool.py
~~~

## Key idea

The first script asks a model for one answer. The second script gives the model
a greet tool. When the model decides to use it, LangGraph runs the tool and
returns its result to the model for the final response.
