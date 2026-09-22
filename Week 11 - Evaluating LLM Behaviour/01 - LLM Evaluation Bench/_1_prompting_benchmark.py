# What this file does: compares prompting strategies for answer quality and token cost.

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MODEL_ID = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
BENCHMARK_QUESTIONS = [
    (
        "A shop sells pens for 23 rupees each. Ravi buys 7 pens, returns 2, then buys 4 more. He pays with 500 rupees. How much change does he receive?",
        "293",
    ),
    (
        "A jacket costs 4000 rupees. Apply a 25% discount, then 10% off the reduced price, then add 18% GST. What is the final price?",
        "3186",
    ),
    (
        "A factory makes 2000 units. Eight percent fail quality control. Fifteen percent of the rest are exported. How many are sold domestically?",
        "1564",
    ),
    (
        "A train leaves at 14:35, travels for 3 hours 50 minutes, waits 25 minutes, then travels 1 hour 40 minutes. When does it arrive in 24-hour HH:MM format?",
        "20:30",
    ),
    (
        "Three printers make 90 pages in 6 minutes. At the same rate, how many pages do 5 printers make in 10 minutes?",
        "250",
    ),
]
FEW_SHOT_EXAMPLES = """Example:
Question: A baker makes 12 loaves, sells 5, then makes 8 more. How many loaves are left?
Reasoning: Start with 12. After selling 5, 7 remain. Add 8, so 15 remain.
Answer: 15"""
PROMPT_STRATEGIES = {
    "Direct": "Answer with only the final value.\n\nQuestion: {question}",
    "Zero-shot reasoning": (
        "Work through the calculation briefly. End with `Answer: <value>`.\n\n"
        "Question: {question}"
    ),
    "Few-shot reasoning": (
        "{examples}\n\nWork through the calculation briefly. End with "
        "`Answer: <value>`.\n\nQuestion: {question}"
    ),
}


def create_client() -> OpenAI:
    """Create an authenticated client after checking the required key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from the Week 11 .env file.")
    return OpenAI(api_key=api_key)


def ask_model(client: OpenAI, prompt: str) -> tuple[str, int]:
    """Send one prompt and return its text with the total reported token count."""
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    usage = response.usage
    total_tokens = (usage.prompt_tokens if usage else 0) + (
        usage.completion_tokens if usage else 0
    )
    return response.choices[0].message.content or "", total_tokens


def final_answer(response: str) -> str:
    """Extract the final answer instead of scoring numbers inside reasoning text."""
    answer_markers = list(re.finditer(r"answer\s*:", response, flags=re.IGNORECASE))
    if answer_markers:
        text = response[answer_markers[-1].end() :]
    else:
        lines = [line for line in response.splitlines() if line.strip()]
        text = lines[-1] if lines else ""
    return text.strip().splitlines()[0].strip().lower() if text.strip() else ""


def is_correct(response: str, expected_answer: str) -> bool:
    """Check the first value in the model's stated conclusion."""
    stated_answer = final_answer(response).replace(",", "")
    expected = expected_answer.lower()
    if stated_answer.rstrip(".") == expected:
        return True
    numbers = re.findall(r"\d+(?:\.\d+)?", stated_answer)
    return bool(numbers) and numbers[0] == expected


def print_results(results: dict[str, dict[str, int]]) -> None:
    """Print a compact comparison that keeps quality and cost together."""
    print(f"\nModel: {MODEL_ID}\n")
    print(f"{'Strategy':<22} {'Correct':>9} {'Accuracy':>10} {'Tokens':>9} {'Avg/query':>11}")
    print("-" * 67)
    for name, data in results.items():
        accuracy = data["correct"] / len(BENCHMARK_QUESTIONS) * 100
        average_tokens = data["tokens"] / len(BENCHMARK_QUESTIONS)
        print(
            f"{name:<22} {data['correct']:>4}/{len(BENCHMARK_QUESTIONS):<4} "
            f"{accuracy:>8.0f}% {data['tokens']:>9} {average_tokens:>11.1f}"
        )


def main() -> None:
    """Run every question with every prompting strategy."""
    client = create_client()
    results = {name: {"correct": 0, "tokens": 0} for name in PROMPT_STRATEGIES}

    for strategy_name, template in PROMPT_STRATEGIES.items():
        print(f"\n{strategy_name}")
        for question_number, (question, expected_answer) in enumerate(
            BENCHMARK_QUESTIONS, start=1
        ):
            prompt = template.format(question=question, examples=FEW_SHOT_EXAMPLES)
            response, tokens = ask_model(client, prompt)
            correct = is_correct(response, expected_answer)
            results[strategy_name]["correct"] += int(correct)
            results[strategy_name]["tokens"] += tokens
            print(
                f"  {question_number}. {'correct' if correct else 'wrong'} "
                f"| answer: {final_answer(response)!r} | {tokens} tokens"
            )

    print_results(results)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
