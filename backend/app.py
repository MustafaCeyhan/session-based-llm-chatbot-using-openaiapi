from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from datetime import datetime
import logging
import sqlite3

from dotenv import load_dotenv
_ = load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("conversations.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            session_id TEXT,
            role TEXT,
            content TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Function to save a conversation
def save_conversation(session_id, role, content):
    conn = sqlite3.connect("conversations.db", check_same_thread=False)
    cursor = conn.cursor()
    date = datetime.now()
    cursor.execute('''
        INSERT INTO conversations (session_id, role, content, date) VALUES (?, ?, ?, ?)
    ''', (session_id, role, content, date))
    conn.commit()
    conn.close()

# Call this function once to initialize the database
init_db()

# Model to capture the question, history, session ID, and OpenAI API key
class Query(BaseModel):
    question: str
    history: list = []  # This will hold the past conversation
    session_id: str  # This will hold the session ID
    openai_api_key: str  # This will hold the OpenAI API key provided by the user

# Initialize conversation buffer memory
memory = ConversationBufferMemory(return_messages=True)

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI helpful assistant."),
    ("human", "{input}"),
])

def ask_llm(state):
    try:
        # Initialize the ChatOpenAI model with the provided API key
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=state["openai_api_key"])

        # Create the chain
        chain = (
            {"input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # Use .get() to avoid KeyError and default to an empty list if history is not provided
        for msg in state.get("history", []):
            if msg["role"] == "user":
                memory.chat_memory.add_user_message(msg["content"])
            else:
                memory.chat_memory.add_ai_message(msg["content"])

        # Add the new question to memory
        memory.chat_memory.add_user_message(state["question"])

        # Invoke the chain
        response = chain.invoke({
            "input": state["question"],
            "history": memory.chat_memory.messages  # Pass full conversation history
        })

        # Add the response to memory
        memory.chat_memory.add_ai_message(response)

        # Save the conversation in the SQLite database
        save_conversation(state["session_id"], "user", state["question"])
        save_conversation(state["session_id"], "assistant", response)

        # Return the AI response and updated history
        return {
            "response": response,
            "history": memory.chat_memory.messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to receive the question, history, session ID, and OpenAI API key
@app.post("/llm")
def ask_question(query: Query):
    logger.info(f"Received query for {query.session_id} session id: {query.question}")
    response = ask_llm(query.dict())
    logger.info(f"Response: {response['response']}")
    return response

# If you're running the app directly, you can uncomment this:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)