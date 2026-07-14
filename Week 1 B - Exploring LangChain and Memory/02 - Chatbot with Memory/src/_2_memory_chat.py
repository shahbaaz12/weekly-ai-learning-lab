import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

# Load the API configuration once when the chat program starts.
load_dotenv()

model = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature=0.3,
)

# Insert the growing history between the system instruction and new question.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a friendly assistant. "
            "Use the conversation history to stay consistent.",
        ),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)

# This pipeline returns an AIMessage for each user question.
chain = prompt | model
# Memory starts empty and exists only while this program is running.
history = []

print("Chat with the bot. Type 'quit' to exit.")

while True:
    # Read one new message from the terminal.
    question = input("You: ").strip()

    if question.lower() in {"quit", "exit"}:
        break

    if not question:
        continue

    # Re-send every previous turn so the model can use the conversation context.
    answer = chain.invoke(
        {"history": history, "question": question}
    ).content

    print("Bot:", answer)

    # Save both sides of this turn for the next request.
    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=answer))

    print(f"(History: {len(history)} messages)")
