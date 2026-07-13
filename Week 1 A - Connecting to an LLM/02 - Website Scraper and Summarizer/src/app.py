import gradio as gr

# Keep the AI and scraping logic separate from the user interface.
from summarizer import summarize


def summarize_url(url: str) -> str:
    """Return a user-friendly message if summarization fails."""
    # Gradio calls this function whenever the user submits a URL.
    try:
        return summarize(url)
    except Exception as error:
        return f"## Could not summarize this website\n\n{error}"


# Describe the input, output, examples, and appearance of the web app.
demo = gr.Interface(
    fn=summarize_url,
    inputs=gr.Textbox(
        label="Website URL",
        placeholder="https://www.python.org/",
    ),
    outputs=gr.Markdown(label="Summary"),
    title="AI Website Summarizer",
    description="Enter a public website URL to receive an AI-generated summary.",
    examples=[
        ["https://www.python.org/"],
        ["https://example.com/"],
    ],
    flagging_mode="never",
)


if __name__ == "__main__":
    # Starts a local app. It is not publicly shared.
    demo.launch()
