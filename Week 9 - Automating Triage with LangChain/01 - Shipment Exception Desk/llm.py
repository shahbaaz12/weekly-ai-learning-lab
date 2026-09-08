# What this file does: builds the one chat model every chain in this project shares.

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()

# Switch this to "openai" and set OPENAI_API_KEY to use OpenAI instead.
PROVIDER = "groq"
MODELS = {
    "groq": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    "openai": "gpt-4o-mini",
}


def get_model():
    """Return the shared chat model, named as provider:model for init_chat_model."""
    key_name = "GROQ_API_KEY" if PROVIDER == "groq" else "OPENAI_API_KEY"

    if not os.getenv(key_name):
        raise RuntimeError(f"{key_name} is missing from .env.")

    # Temperature 0 keeps classification stable, which the routing depends on.
    return init_chat_model(f"{PROVIDER}:{MODELS[PROVIDER]}", temperature=0)
