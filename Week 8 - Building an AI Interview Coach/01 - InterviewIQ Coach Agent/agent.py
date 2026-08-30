# What this file does: the evaluator agent - tool calling, session memory, and the aggregated report.
"""InterviewIQ evaluator agent."""

import json
import os

from dotenv import load_dotenv
from openai import BadRequestError, OpenAI

from tools import check_star_structure, detect_filler_words, score_relevance


load_dotenv()
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# The model calls one tool per round, so three tools need three rounds and a
# fourth to write the feedback. Five leaves headroom and still cannot run away.
MAX_TOOL_ROUNDS = 5

# gpt-oss sometimes leaks a format token into the tool name, which Groq rejects
# as an unknown tool. It is random sampling noise, so asking again clears it.
MAX_GLITCH_RETRIES = 3

EVALUATOR_PROMPT = """
You are InterviewIQ, a warm and practical mock-interview coach.

Call the tools that fit the answer you were given. Use score_relevance on every
answer. Use check_star_structure when the question asks about a past experience.
Use detect_filler_words when the answer sounds spoken or padded.

Then write feedback for the candidate in three short sentences or fewer:
one thing they did well, one specific thing to fix, and a warm closing line.
Quote the tool numbers you were given. Never invent a score.
"""

COACH_PROMPT = """
You are InterviewIQ, a mock-interview coach answering a question about the
candidate's own session.

Answer only from the session facts you are given. Those numbers are already
calculated, so never recompute or guess them. When you are asked about the
weakest area, name the exact question listed as the weakest area, even when it
is not the most recent one. Keep the reply under five sentences and encouraging.
"""

# The tools take no arguments on purpose. The agent decides which ones to run,
# and this file supplies the real answer and keywords, so a score is always
# measured from the candidate's actual words instead of the model's summary.
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "detect_filler_words",
            "description": "Count filler words such as 'um', 'like', and 'basically'.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_star_structure",
            "description": "Check whether the answer covers Situation, Task, Action, Result.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "score_relevance",
            "description": "Score 0-100 how well the answer covers the question's expected topics.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


class InterviewCoach:
    """Evaluates each answer with tools and remembers the whole session."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.evaluations = []
        self._client = None

    @property
    def client(self) -> OpenAI:
        """Create the Groq client the first time it is needed."""
        if self._client is None:
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                raise RuntimeError("GROQ_API_KEY is missing from .env.")

            self._client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)

        return self._client

    def _create(self, **kwargs):
        """Send one request, retrying the random Groq tool-name glitch."""
        last_error = None

        for _ in range(MAX_GLITCH_RETRIES):
            try:
                return self.client.chat.completions.create(**kwargs)
            except BadRequestError as error:
                if getattr(error, "code", None) != "tool_use_failed":
                    raise
                last_error = error

        raise last_error

    def evaluate_answer(self, question: dict, answer: str) -> str:
        """Run the tool loop on one answer, remember it, and return short feedback."""
        runners = {
            "detect_filler_words": lambda: detect_filler_words(answer),
            "check_star_structure": lambda: check_star_structure(answer),
            "score_relevance": lambda: score_relevance(
                answer, question["expected_keywords"]
            ),
        }

        messages = [
            {"role": "system", "content": EVALUATOR_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Interview question: {question['question']}\n\n"
                    f"Candidate answer: {answer}"
                ),
            },
        ]

        results = {}

        # Keep the tools on every call. Groq rejects a follow-up call that omits
        # them if the model still wants a tool, so the loop ends only when the
        # model replies with plain feedback instead.
        for _ in range(MAX_TOOL_ROUNDS):
            message = self._create(
                model=self.model,
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
            ).choices[0].message

            if not message.tool_calls:
                break

            messages.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                runner = runners.get(name)
                results[name] = runner() if runner else {"error": "Unknown tool."}
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(results[name]),
                    }
                )

        feedback = message.content or "No feedback returned."

        # The scorecard and the weakest-area report need a relevance score for
        # every answer, so measure it here when the model did not ask for it.
        if "score_relevance" not in results:
            results["score_relevance"] = runners["score_relevance"]()

        self._remember(question, answer, results, feedback)
        return feedback

    def _remember(
        self, question: dict, answer: str, results: dict, feedback: str
    ) -> None:
        """Save one evaluated turn so later turns can still see it."""
        relevance = results["score_relevance"]
        filler = results.get("detect_filler_words", {})
        star = results.get("check_star_structure", {})

        self.evaluations.append(
            {
                "question_id": question["id"],
                "question": question["question"],
                "category": question["category"],
                "answer": answer,
                "relevance_score": relevance["score"],
                "missing_keywords": relevance["missing_keywords"],
                "filler_count": filler.get("filler_count", 0),
                "star_missing": star.get("components_missing", []),
                "feedback": feedback,
            }
        )

    def session_summary(self) -> dict:
        """Aggregate the session. Python calculates these numbers, never the model."""
        if not self.evaluations:
            return {"answered": 0}

        scores = [item["relevance_score"] for item in self.evaluations]
        weakest = min(self.evaluations, key=lambda item: item["relevance_score"])
        strongest = max(self.evaluations, key=lambda item: item["relevance_score"])

        return {
            "answered": len(self.evaluations),
            "average_relevance": round(sum(scores) / len(scores), 1),
            "weakest_question": weakest["question"],
            "weakest_question_id": weakest["question_id"],
            "weakest_score": weakest["relevance_score"],
            "strongest_question": strongest["question"],
            "strongest_score": strongest["relevance_score"],
            "total_fillers": sum(item["filler_count"] for item in self.evaluations),
        }

    def scorecard_rows(self) -> list[list]:
        """Return one row per answered question, for the live scorecard."""
        return [
            [
                item["question"],
                item["category"],
                item["relevance_score"],
                item["filler_count"],
                ", ".join(item["star_missing"]) or "-",
            ]
            for item in self.evaluations
        ]

    def _session_digest(self) -> str:
        """Format the already-calculated session facts for the model to read."""
        summary = self.session_summary()
        weakest = f"{summary['weakest_question']} ({summary['weakest_score']}/100)"
        strongest = f"{summary['strongest_question']} ({summary['strongest_score']}/100)"

        lines = [
            f"Questions answered: {summary['answered']}",
            f"Average relevance score: {summary['average_relevance']}/100",
            f"Weakest area, the lowest score of the session: {weakest}",
            f"Strongest answer: {strongest}",
            f"Total filler words across the session: {summary['total_fillers']}",
            "",
            "Every answer so far, in order:",
        ]

        for item in self.evaluations:
            missing = ", ".join(item["star_missing"]) or "nothing"
            lines.append(
                f"- {item['question']} | relevance {item['relevance_score']}/100 "
                f"| fillers {item['filler_count']} | STAR missing: {missing}"
            )

        return "\n".join(lines)

    def ask_agent(self, user_question: str) -> str:
        """Answer a meta-question from the whole session, at any point mid-interview."""
        if not self.evaluations:
            return "No answers yet. Answer one question and I can tell you how it is going."

        response = self._create(
            model=self.model,
            messages=[
                {"role": "system", "content": COACH_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Session so far:\n{self._session_digest()}\n\n"
                        f"The candidate asks: {user_question}"
                    ),
                },
            ],
        )

        return response.choices[0].message.content or "No answer returned."

    def generate_final_report(self) -> str:
        """Build the aggregated report: average score, named weakest area, observations."""
        if not self.evaluations:
            return "No answers yet, so there is nothing to report."

        summary = self.session_summary()

        # Python writes the numbers below. The model only adds the prose, so a
        # weak model can never change the average or the named weakest area.
        observations = self.ask_agent(
            "Write two or three sentences of overall observations about this "
            "session, and one concrete thing to practise next."
        )

        return (
            "## InterviewIQ final report\n\n"
            f"- **Questions answered:** {summary['answered']}\n"
            f"- **Average relevance score:** {summary['average_relevance']}/100\n"
            f"- **Weakest area:** {summary['weakest_question']} "
            f"({summary['weakest_score']}/100)\n"
            f"- **Strongest answer:** {summary['strongest_question']} "
            f"({summary['strongest_score']}/100)\n"
            f"- **Total filler words:** {summary['total_fillers']}\n\n"
            "### Observations\n\n"
            f"{observations}"
        )


# The check scripts and the multi-agent demo import these module-level names and
# do not manage a coach of their own, so they share one session. The Gradio app
# builds its own InterviewCoach per browser session instead.
_default_coach = InterviewCoach()

# Iterate this to watch memory accumulate. Entries use the shape built in _remember.
session_log = _default_coach.evaluations


def run_turn(question: str, answer: str, expected_keywords: list) -> str:
    """Evaluate one answer for a plain question string and remember the turn."""
    return _default_coach.evaluate_answer(
        {
            "id": question,
            "question": question,
            "category": "general",
            "expected_keywords": expected_keywords,
        },
        answer,
    )


def ask_agent(user_message: str) -> str:
    """Answer a meta-question about the shared session, at any point."""
    return _default_coach.ask_agent(user_message)


def generate_final_report() -> str:
    """Return the aggregated report for the shared session."""
    return _default_coach.generate_final_report()


def ask_for_final_report() -> str:
    """Name the CLI and the multi-agent demo use for the final report."""
    return generate_final_report()


def reset_session() -> None:
    """Forget the shared session, so a script can start a fresh interview."""
    _default_coach.evaluations.clear()
