import gradio as gr

# Keep tool-calling logic in agent.py and the user interface in this file.
from agent import agent


def chat(message, history):
    # Gradio provides the newest message; this first version does not store UI history.
    try:
        return agent(message)
    except Exception as error:
        return f"Something went wrong: {error}"


# Build the browser chat interface around the Python chat function.
demo = gr.ChatInterface(
    fn=chat,
    title="Smart Shop Assistant",
    description="Ask the price of shoes, hat, bag, shorts, or pants.",
)


if __name__ == "__main__":
    demo.launch()
