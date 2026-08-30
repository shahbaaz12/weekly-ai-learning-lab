# What this file does: checks the Groq key works by making one plain LLM call, before any tools exist.

import os

from dotenv import load_dotenv
from openai import OpenAI

from interview_bank import QUESTIONS


load_dotenv()
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def main() -> None:
    api_key = os.getenv("GROQ_API_KEY")

    # Fail with the exact missing name rather than a confusing API error.
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from .env.")

    client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: InterviewIQ setup looks good.",
            }
        ],
    )

    print(f"Questions loaded: {len(QUESTIONS)}")
    print(f"Model: {MODEL}")
    print(f"Model replied: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
