import os

from dotenv import load_dotenv
from openai import OpenAI

# Load the API settings stored in the local .env file.
load_dotenv()
 
 
# Groq supports the OpenAI API format, so the OpenAI client can talk to Groq.
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), #groq api key
    base_url=os.getenv("GROQ_API_BASE_URL"),
)

# Send one prompt to the model and keep its full response object.
response = client.responses.create(
    model="openai/gpt-oss-120b",
    instructions="You are a witty assistant",
    input="Suggest one excuse for being late to office.",
)

# Print only the text returned by the model.
print(response.output_text)

#checking the available models
# models = client.models.list()

# for model in models.data:
#     print(model.id)
 
