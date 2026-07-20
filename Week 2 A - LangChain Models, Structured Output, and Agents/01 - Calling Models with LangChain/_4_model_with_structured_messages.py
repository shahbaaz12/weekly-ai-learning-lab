from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool


# --- This can be your service/repo or an api call ---
@tool
def check_stock_service(item: str) -> str:
    """This function can be used to check the remaining stock quantity"""
    dbContext = {
        "headphone": 6,
        "keyboard": 11,
        "laptop": 12,
    }
    return f"{item} has {dbContext[item]} quantity of stock"


# --- Initialize a model ---

load_dotenv()

model = init_chat_model(
    "groq:openai/gpt-oss-120b",
    temperature=0,
).bind_tools([check_stock_service])

messages = [
    SystemMessage("You are a stock keeper assistant."),
    HumanMessage("How many keyboards do we have remaining?"),
]

response = model.invoke(messages)
messages.append(response)  # preserving the ai response

# --- The response may have a tool call ---

if response.tool_calls:
    tool_message = check_stock_service.invoke(response.tool_calls[0])
    messages.append(tool_message)  # preserving the tool response
    response = model.invoke(messages)

print(response.content)
