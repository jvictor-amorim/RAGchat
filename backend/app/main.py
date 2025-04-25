import os
import pandas as pd
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Qdrant
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)
API_KEY_LLM = os.getenv("API_KEY_LLM")
from pathlib import Path
current_dir = Path(__file__).parent
data_dir = current_dir.parent / "data"
data_path = data_dir / "casos.csv"
df = pd.read_csv(data_path)

chat_model = ChatOpenAI(
    model='llama3-8b-8192',
    base_url="https://api.groq.com/openai/v1", 
    api_key=API_KEY_LLM,
    temperature=0.7
)

df_3_rows = df.iloc[0:3]
loader = DataFrameLoader(df_3_rows, page_content_column="historia")
documents = loader.load()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

qdrant = Qdrant.from_documents(
    documents=documents,
    embedding=embeddings,
    location=":memory:",
    collection_name="chatbot"
)

messagesContextRAG = [
    SystemMessage(content="Você é um assistente útil que responde perguntas."),
]

messagesContextDefault = [
    SystemMessage(content="Você é um assistente útil que responde perguntas."),
]

def custom_prompt(query: str):
    results = qdrant.similarity_search(query, k=3)
    source_knowledge = "\n".join([x.page_content for x in results])
    augment_prompt = f"""Use o contexto abaixo para responder à pergunta.

    Contexto:
    {source_knowledge}

    Pergunta: {query}"""
    return augment_prompt

class ChatRequest(BaseModel):
    message: str
    type: str

@app.post("/chat/")
async def chat_endpoint(chat_request: ChatRequest):
    res = ''
    if chat_request.type == "RAG":
        prompt_customize = custom_prompt(chat_request.message)
        messagesContextRAG.append(HumanMessage(content=prompt_customize))
        res = chat_model.invoke(messagesContextRAG)
        messagesContextRAG.append(AIMessage(content=res.content))
    else:
        messagesContextDefault.append(HumanMessage(content=chat_request.message))
        res = chat_model.invoke(messagesContextDefault)
        messagesContextDefault.append(AIMessage(content=res.content))
    return {"response": res.content}