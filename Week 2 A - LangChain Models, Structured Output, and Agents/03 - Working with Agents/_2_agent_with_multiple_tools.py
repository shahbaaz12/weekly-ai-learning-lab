from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


@tool
def check_stock_service(item: str) -> str:
    """Check the remaining stock quantity of an item."""
    stock = {"headphone": 6, "keyboard": 11, "laptop": 12}
    return f"{item} has {stock.get(item, 0)} units left."


@tool
def get_price_service(item: str) -> str:
    """Get the price of an item."""
    prices = {"headphone": 1999, "keyboard": 1499, "laptop": 54999}
    return f"{item} costs Rs {prices.get(item, 0)}."


messages = [
    SystemMessage("You are a helpful inventory assistant. "),
    HumanMessage("Do we have laptops in stock, and what is the price?"),
]

model = init_chat_model(model="groq:openai/gpt-oss-120b")

agent = create_agent(model=model, tools=[check_stock_service, get_price_service])

response = agent.invoke({"messages": messages})

# --- printing ---
for message in response["messages"]:
    print(f"{type(message).__name__} :: {message.content}")
