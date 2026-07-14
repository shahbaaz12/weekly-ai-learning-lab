import json
import os

from dotenv import load_dotenv
from groq import Groq

from shop_database import get_price

# Load the Groq key and model name from .env.
load_dotenv()

# Create one reusable API client for all agent requests.
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Describe the Python tool so the model knows when and how to call it.
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "Get the price of a shop item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The item name",
                    }
                },
                "required": ["item"],
                "additionalProperties": False,
            },
        },
    }
]


def agent(user_message: str) -> str:
    # Stop early with a clear message if the secret was not configured.
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is missing from .env.")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful shop assistant. "
                "Use the get_price tool whenever the user asks about a price."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    # First model call: it can either answer directly or request a tool.
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message # the model's first response, which may include a tool call

    # A normal chat response does not need a second model call.
    if not message.tool_calls:
        return message.content or "I could not generate a response."

    # Preserve the model's tool request in the conversation.
    messages.append(message)

    # there could be multiple tool calls, so we loop through them all
        #eg : for a shirt, or pants, or shoes, the model may call the tool multiple times to get prices for each item
    for tool_call in message.tool_calls: 
        # Decode the JSON arguments, then run the matching Python function.
        arguments = json.loads(tool_call.function.arguments)

        if tool_call.function.name == "get_price":
            result = get_price(arguments["item"])
        else:
            result = "That tool is unavailable."

        # Return the tool result using the required "tool" message role.
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

    # Second model call: turn the tool result into a friendly final answer.
    final_response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        messages=messages,
    )

    return final_response.choices[0].message.content or "No response returned."


if __name__ == "__main__":
    print(agent("How much are the shoes?"))
