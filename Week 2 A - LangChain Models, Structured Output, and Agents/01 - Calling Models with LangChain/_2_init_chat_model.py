from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

gemini_model_name = "google_genai:gemini-3.1-flash-lite-preview"
groq_model_name = "groq:openai/gpt-oss-120b"


# --- 1. Invoking Gemini model ---
print("--- Gemini ---")

model = init_chat_model(model=gemini_model_name)
response = model.invoke(
    "Suggest snarky comeback for a manager assigning last minute task"
)
print(response.content)

# --- 2. Invoking GROQ model ---
print("--- GROQ ---")

model = init_chat_model(model=groq_model_name)
response = model.invoke(
    "Suggest snarky comeback for a manager assigning last minute task"
)
print(response.content)
