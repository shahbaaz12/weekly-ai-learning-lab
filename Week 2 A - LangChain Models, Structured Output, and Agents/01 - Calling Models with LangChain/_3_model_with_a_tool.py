from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()


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

model = init_chat_model(model="groq:openai/gpt-oss-120b")

model_with_tool = model.bind_tools([check_stock_service])  # make model aware of a tool

response = model_with_tool.invoke("How many keyboards do we have remaining")

# --- The response may have a tool call ---

if response.tool_calls:
    args_for_tool = response.tool_calls[0]["args"]["item"]
    result = check_stock_service.invoke(args_for_tool)
    print(result)
    response = model_with_tool.invoke(result)  # pass the tool result back to the model
print(response.content)
