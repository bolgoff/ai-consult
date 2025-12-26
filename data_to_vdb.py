import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
<<<<<<< HEAD
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import settings

QDRANT_URL = settings.QDRANT_URL
COLLECTION_NAME = settings.QDRANT_COLLECTION_NAME
=======
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333") 
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "knowledge_base")
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
FILE_PATH = "data/all_data.txt"

def transfer():
    loader = TextLoader(FILE_PATH, encoding="utf-8")
    docs = loader.load()
<<<<<<< HEAD
    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=25)
=======
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
    chunks = splitter.split_documents(docs)

    client = QdrantClient(url=QDRANT_URL)
    
<<<<<<< HEAD
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )

    embeddings = OllamaEmbeddings(
	model="nomic-embed-text",
	base_url="http://ollama:11434"
)
    
    try:
        QdrantVectorStore.from_documents(
            chunks,
            embeddings,
            url=QDRANT_URL,
            collection_name=COLLECTION_NAME
        )
        print("###загрузка в qdrant выполнена###")
    except:
        print("error")

if __name__ == "__main__":
    transfer()
=======
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    QdrantVectorStore.from_documents(
        chunks,
        embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )
    print("###загрузка в qdrant выполнена###")

if __name__ == "__main__":
    transfer()
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
