import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
from crewai import Task, Agent, Crew, Process, LLM
from functools import lru_cache

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = "finance-chatbot"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2', cache_folder="/tmp")

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name=COLLECTION_NAME
)

mistral_llm = LLM(model="mistral/mistral-large-latest", api_key=MISTRAL_API_KEY, temperature=0.7)

gemini_llm = LLM(model="gemini/gemini-2.0-flash", api_key=GEMINI_API_KEY, temperature=0.7)

# Functions
@lru_cache(maxsize=100)
def search_qdrant(query, top_k=3):
    '''Search Qdrant for documents'''
    try:
        retreiver = qdrant.as_retriever(search_type='similarity', search_kwargs={"k": top_k})
        results = retreiver.invoke(query)
        return [{"text": doc.page_content, "source": doc.metadata.get("source", "Unknown")} for doc in results]
    except Exception:
        return []
    