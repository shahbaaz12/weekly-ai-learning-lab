# Travel Assistant Agent

## Objective

Build one agent that combines multiple tools to plan a simple trip.

## Before running

This project uses the AWS credentials and MODEL_ID from the Week 5 .env file.

## Run

~~~powershell
uv sync
uv run python _1_travel_assistant.py
~~~

You can also pass your own question:

~~~powershell
uv run python _1_travel_assistant.py "I am going to Manali for 4 days with a budget of 15000 rupees. What should I pack?"
~~~

## Key idea

The agent uses the weather tool, packing-list tool, and cost tool together. The
tools use sample data, so you can focus on the agent workflow without needing a
real weather or travel API.
