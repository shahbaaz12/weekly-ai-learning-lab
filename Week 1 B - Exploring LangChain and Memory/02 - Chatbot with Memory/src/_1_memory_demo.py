import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

# Load the model settings used by this small memory example.
load_dotenv()

model = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature=0,
)

 # The history placeholder is where earlier messages will be inserted.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a friendly tutor."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)

# Send the completed prompt to the model.
chain = prompt | model

# This hardcoded conversation demonstrates that memory is just re-sent context.
history = [
    HumanMessage(content="My name is Shbz."),
    HumanMessage(content="My Favorite color is white."),
    HumanMessage(content="I love programming."),
    AIMessage(content="Hi Shbz!"),
]

# Ask a question while supplying the earlier conversation.
answer = chain.invoke(
    {"history": history, "question": "What is my preferred color?"}
)

print(answer.content)
