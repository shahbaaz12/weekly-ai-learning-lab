# What this file does: checks the key and the model work by running one chain, before any logic exists.

from chains import classify_chain
from llm import MODELS, PROVIDER


SAMPLE_REPORT = "The pallet arrived three days late and the client is unhappy."


def main() -> None:
    print(f"Provider: {PROVIDER}")
    print(f"Model: {MODELS[PROVIDER]}")

    category = classify_chain.invoke({"report": SAMPLE_REPORT})
    print(f"Classified the sample report as: {category.strip()}")


if __name__ == "__main__":
    main()
