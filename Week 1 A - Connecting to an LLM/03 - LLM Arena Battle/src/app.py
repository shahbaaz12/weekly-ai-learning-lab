import gradio as gr

# Import the model-comparison logic; this file only builds the interface.
from arena import battle


def run_battle(prompt: str) -> tuple[str, str, str]:
    """Run both models and return answers for the UI."""
    # Return errors as text so the Gradio page stays usable.
    try:
        answer_a, answer_b = battle(prompt)
        return answer_a, answer_b, ""
    except Exception as error:
        return "", "", f"## Battle failed\n\n{error}"


def vote(model_label: str) -> str:
    """Show the selected winner for this demo session."""
    return f"### Vote recorded\n\nYou chose **{model_label}**."


with gr.Blocks(title="LLM Arena Battle") as demo:
    # Build a small blind-comparison interface for two model responses.
    gr.Markdown("# LLM Arena Battle")
    gr.Markdown(
        "Send one prompt to two models, compare their answers, then vote."
    )

    prompt = gr.Textbox(
        label="Your prompt",
        placeholder="Ask both models the same question...",
        lines=3,
    )
    battle_button = gr.Button("Start Battle", variant="primary")

    # Keep model identities hidden to make voting fair.
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Model A")
            output_a = gr.Markdown()
            vote_a = gr.Button("Vote for Model A")

        with gr.Column():
            gr.Markdown("## Model B")
            output_b = gr.Markdown()
            vote_b = gr.Button("Vote for Model B")

    status = gr.Markdown()

    # Connect each button to the Python function it should run.
    battle_button.click(
        fn=run_battle,
        inputs=prompt,
        outputs=[output_a, output_b, status],
    )
    vote_a.click(fn=lambda: vote("Model A"), outputs=status)
    vote_b.click(fn=lambda: vote("Model B"), outputs=status)


if __name__ == "__main__":
    # Start locally; add share=True only when you intentionally want a public URL.
    demo.launch()
