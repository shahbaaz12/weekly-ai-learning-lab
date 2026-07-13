import os

from dotenv import load_dotenv
from openai import OpenAI

# Load values from the local .env file.
load_dotenv()

# Give both models the same behavior instructions.
SYSTEM_PROMPT = """
You are participating in a blind LLM comparison.
Answer the user's prompt clearly, helpfully, and directly.
Do not mention your model name or provider.
"""


def create_client() -> OpenAI:
    """Create a Groq client using the values from .env."""
    api_key = os.getenv("GROQ_API_KEY")
    base_url = os.getenv("GROQ_API_BASE_URL")

    if not api_key or not base_url:
        raise RuntimeError(
            "GROQ_API_KEY or GROQ_API_BASE_URL is missing from .env."
        )

    # Send requests through Groq's OpenAI-compatible endpoint.
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
    )


def ask(client: OpenAI, model: str, prompt: str) -> str:
    """Send one prompt to one model and return its answer."""
    # Both models receive the same system instructions and user prompt.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        # Same temperature keeps the comparison fair.
        temperature=0.7,
    )

    return response.choices[0].message.content or "No text response returned."


def battle(prompt: str) -> tuple[str, str]:
    """Send the same prompt to both arena models."""
    # Remove extra whitespace before checking the user's input.
    prompt = prompt.strip()

    if not prompt:
        raise ValueError("Enter a prompt before starting a battle.")

    # Read the two model IDs from .env.
    model_a = os.getenv("GROQ_MODEL_A")
    model_b = os.getenv("GROQ_MODEL_B")

    if not model_a or not model_b:
        raise RuntimeError(
            "GROQ_MODEL_A or GROQ_MODEL_B is missing from .env."
        )

    client = create_client()

    # Both models receive exactly the same prompt.
    answer_a = ask(client, model_a, prompt)
    answer_b = ask(client, model_b, prompt)

    # The UI shows these as anonymous Model A and Model B answers.
    return answer_a, answer_b
