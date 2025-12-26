<<<<<<< HEAD
from langchain_ollama import OllamaEmbeddings
=======
from langchain_openai import OpenAIEmbeddings
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.config import settings

def get_vectors():
    client = QdrantClient(url=settings.QDRANT_URL)
<<<<<<< HEAD
    embeddings = OllamaEmbeddings(
	model='nomic-embed-text',
	base_url="http://ollama:11434")

    vector_base = QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        embedding=embeddings,
    )
    
    return vector_base
=======
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    
    vector_base = QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        embeddings=embeddings,
    )
    
    return vector_base
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
