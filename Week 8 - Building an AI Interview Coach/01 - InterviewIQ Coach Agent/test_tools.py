# What this file does: tests the three tools directly, with no agent and no LLM call.

from interview_bank import QUESTIONS_BY_ID
from tools import check_star_structure, detect_filler_words, score_relevance


WEAK_ANSWER = "Um, I would basically like, you know, just restart it and hope."

STRONG_ANSWER = (
    "When I was working on the checkout service last year, our team saw 500 errors "
    "in production. I had to find the cause quickly. So I started with the logs and "
    "our monitoring dashboard, then tried to reproduce the failure locally. I found "
    "the root cause was a bad database migration, so I decided to trigger a rollback "
    "and ship a fix. As a result the errors stopped within twenty minutes and we "
    "learned to add a migration check."
)


def show(title: str, result: dict) -> None:
    """Print one tool result as readable lines."""
    print(f"\n--- {title} ---")
    for key, value in result.items():
        print(f"{key}: {value}")


def main() -> None:
    question = QUESTIONS_BY_ID["debug-production"]
    keywords = question["expected_keywords"]

    print("Question:", question["question"])

    # 1. Filler words: the weak answer is padded, the strong one is clean.
    weak_filler = detect_filler_words(WEAK_ANSWER)
    strong_filler = detect_filler_words(STRONG_ANSWER)
    show("detect_filler_words on the weak answer", weak_filler)
    show("detect_filler_words on the strong answer", strong_filler)

    assert weak_filler["filler_count"] >= 3, "Expected several fillers in the weak answer."
    assert strong_filler["filler_count"] == 0, "Strong answer should have no fillers."

    # 2. STAR structure: only the strong answer tells a complete story.
    weak_star = check_star_structure(WEAK_ANSWER)
    strong_star = check_star_structure(STRONG_ANSWER)
    show("check_star_structure on the weak answer", weak_star)
    show("check_star_structure on the strong answer", strong_star)

    assert not weak_star["star_complete"], "Weak answer should be missing components."
    assert strong_star["star_complete"], "Strong answer should cover all four parts."

    # 3. Relevance: the strong answer hits the question's expected keywords.
    weak_relevance = score_relevance(WEAK_ANSWER, keywords)
    strong_relevance = score_relevance(STRONG_ANSWER, keywords)
    show("score_relevance on the weak answer", weak_relevance)
    show("score_relevance on the strong answer", strong_relevance)

    assert weak_relevance["score"] < 40, "Weak answer should score low."
    assert strong_relevance["score"] > 80, "Strong answer should score high."

    # 4. An empty answer must not crash the division in detect_filler_words.
    empty = detect_filler_words("")
    show("detect_filler_words on an empty answer", empty)
    assert empty["filler_ratio"] == 0.0

    print("\nAll tool checks passed.")


if __name__ == "__main__":
    main()
