# Week 5 A - Building AI Agents with AWS Bedrock

## Objective

This week is about AI agents. I learned how an agent can call tools, decide the
order of its work, use shared data, run tools in parallel, and complete a
small travel-planning task.

## What I built

1. **First AI Agents** - Start with a simple Strands agent and then see a LangGraph agent use a tool.
2. **Agent Tools** - Turn normal Python functions into tools for an agent.
3. **Travel Assistant Agent** - Build one agent that checks weather, suggests packing, and estimates trip cost.

## Before running

These projects use Amazon Bedrock. Add your AWS credentials and region to a
Week 5 .env file. You can create it from .env.example.

You also need access to Amazon Nova Lite in the Bedrock console. The default
region in the examples is us-east-1.

## Run a project

Open this Week 5 folder in PowerShell. Each block installs that project's
packages and then runs it.

### 1. First AI Agents

~~~powershell
Push-Location "01 - First AI Agents"
uv sync
uv run python _1_hello_world_agent.py
uv run python _2_langgraph_agent_with_tool.py
Pop-Location
~~~

### 2. Agent Tools

~~~powershell
Push-Location "02 - Agent Tools"
uv sync
uv run python _1_function_to_tool.py
uv run python _2_tip_calculator.py
uv run python _3_sales_agent.py
uv run python _4_inventory_tool.py
uv run python _5_prebuilt_calculator.py
uv run python _6_multiple_prebuilt_tools.py
uv run python _7_aws_tool.py
uv run python _8_class_based_tools.py
uv run python _9_async_tools.py
Pop-Location
~~~

### 3. Travel Assistant Agent

~~~powershell
Push-Location "03 - Travel Assistant Agent"
uv sync
uv run python _1_travel_assistant.py
Pop-Location
~~~
