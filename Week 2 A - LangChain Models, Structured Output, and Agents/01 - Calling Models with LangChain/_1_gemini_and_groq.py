from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


load_dotenv()

gemini_model_name = "gemini-3.1-flash-lite-preview"
groq_model_name = "openai/gpt-oss-120b"

# --- 1. Invoking Gemini model ---
print("--- Gemini ---")
model = ChatGoogleGenerativeAI(model=gemini_model_name)

response = model.invoke("joke for a frustated developer")
print(response.content)

# --- 2. Invoking GROQ model ---
print("--- GROQ ---")
model = ChatGroq(model=groq_model_name)
response = model.invoke("2 lame excuses for a leave")
print(response.content)
