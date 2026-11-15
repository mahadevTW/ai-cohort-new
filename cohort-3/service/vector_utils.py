from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
load_dotenv()  # reads OPENAI_API_KEY from .env
CHROMA_DIR = Path("week3-context/chroma_db")       # Chroma will persist here (just a folder on disk)
EMBED_MODEL = "text-embedding-3-small"  # 1536-dim, cheap ($0.02 / 1M tokens)
client = OpenAI()
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_or_create_collection(name="hr_policies")
def create_embedding(message):
    return client.embeddings.create(model=EMBED_MODEL, input=message).data[0].embedding

def search_vector(message,k=3):
    q_vec = create_embedding(message)
    # search top k chunks from vector
    results = collection.query(query_embeddings=[q_vec], n_results=k,include=["documents", "metadatas"])
    return results

def build_context(message) -> str:
    results = search_vector(message)
    blocks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        blocks.append(f"<source file='{meta['source']}' section='{meta['section']}'>\n{doc}\n</source>")
    return "\n\n".join(blocks)
