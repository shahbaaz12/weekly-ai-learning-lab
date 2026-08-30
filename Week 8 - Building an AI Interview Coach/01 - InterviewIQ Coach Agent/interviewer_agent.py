# What this file does: a second agent whose only job is choosing the next question's category.
"""The Interviewer agent. It never evaluates an answer - that stays in agent.py."""

import os

from dotenv import load_dotenv
from openai import OpenAI

from interview_bank import QUESTIONS


load_dotenv()
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Read the categories from the bank so a new question cannot fall outside them.
CATEGORIES = sorted({question["category"] for question in QUESTIONS})

INTERVIEWER_PROMPT = f"""
You are the Interviewer half of InterviewIQ. Your only job is to choose the
category of the next question from how the candidate has done so far.

Choose one of: {", ".join(CATEGORIES)}.

After a weak answer, stay in the same category so the candidate can try again.
After a strong answer, switch category to test their range.

Reply with the category word and nothing else.
"""


def create_client() -> OpenAI:
    """Create a Groq client using the values from .env."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from .env.")

    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)


def choose_next_category(session_summary: str) -> str:
    """Pick the next question's category. Pass an empty summary for the first turn."""
    client = create_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": INTERVIEWER_PROMPT},
            {
                "role": "user",
                "content": session_summary
                or "This is the first question. Choose a category to start with.",
            },
        ],
    )

    choice = (response.choices[0].message.content or "").strip().lower()

    # The model replies with one word, so match it back onto a real category.
    for category in CATEGORIES:
        if category in choice:
            return category

    return CATEGORIES[0]
