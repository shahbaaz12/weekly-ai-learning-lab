from dotenv import load_dotenv
from langchain.agents import create_agent

from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()


# --- This can be your service/repo or an api call ---
@tool
def check_stock_service(item: str) -> str:
    """This function can be used to check the remaining stock quantity"""
    db_context = {
        "headphone": 6,
        "keyboard": 11,
        "laptop": 12,
    }
    if item not in db_context:
        return f"{item} is not present in the stock database."
    return f"{item} has {db_context[item]} quantity of stock"


# --- Initialize the model ---
model = init_chat_model(model="groq:openai/gpt-oss-120b")
messages = [
    SystemMessage("You are a helpful inventory assistant. "),
    HumanMessage(content="How many laptops do we have ? "),
]


# --- Create the agent ---
agent = create_agent(model=model, tools=[check_stock_service])
response = agent.invoke({"messages": messages})

print(response["messages"][-1].content)
