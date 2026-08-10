# Agent Tools

## Objective

Learn how to give an agent useful Python tools. A good tool has a clear name,
type hints, and a short docstring explaining what it does.

## Before running

This project uses the AWS credentials and MODEL_ID from the Week 5 .env file.

## Run

~~~powershell
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
~~~

## What each script teaches

1. Turn a normal function into an agent tool.
2. Use a tool to calculate and split a tip.
3. Give an agent multiple focused tools for one task.
4. Create a tool for your own inventory data.
5. Use the built-in Strands calculator tool.
6. Combine a web-request tool and calculator tool.
7. Use a read-only AWS tool to list S3 buckets.
8. Keep related tools and their shared data inside a class.
9. Run several tool calls in parallel with an async tool.
