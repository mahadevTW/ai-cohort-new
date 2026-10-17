# read the files from docs folder
# break it down into chunks using sections and subsections, refered from @week3-rag.ipynb
# Every chunk will have the section title prefixed for context 
# embed it using OpenAI embeddings model
# store this into a vector database or a local file for later retrieval at db/chroma
# later, we can query this database to find relevant chunks for a given question

FILE_PATH = "./hr-assistant/docs/it-assets-policy.txt"

from os import path
import chromadb
import re

from openai import OpenAI
openai_client = OpenAI()

CHROMA_DIR = "db/chroma"
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

SECTION_RE = re.compile(r"^=+\n(\d+\.\s+[^\n]+)\n=+\n", re.MULTILINE)   # === / "6. TITLE" / ===
SUBSECTION_RE = re.compile(r"^(?=\d+\.\d+\s)", re.MULTILINE)             # line starting with "6.1 "

def split_sections(text: str) -> list[tuple[str, str]]:
    # re.split with a capture group returns: [preamble, title1, body1, title2, body2, ...]
    parts = SECTION_RE.split(text)
    sections = [("PREAMBLE", parts[0].strip())] if parts[0].strip() else []
    for title, body in zip(parts[1::2], parts[2::2]):
        sections.append((title.strip(), body.strip()))
    return sections

def chunk_document(source: str, text: str, max_tokens: int = 350) -> list[dict]:
    chunks = []
    for section_title, body in split_sections(text):
        subsections = [s.strip() for s in SUBSECTION_RE.split(body) if s.strip()]
        for sub in subsections:
            chunks.append({
                "id": f"{source}::{len(chunks)}",
                "text": f"[{section_title}]\n{sub}",   # section title prefixed for context
                "metadata": {"source": source, "section": section_title, "chunk_index": len(chunks)},
            })
    return chunks

def embed_chunks(chunks: list[dict]) -> list[dict]:
    for chunk in chunks:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["text"]
        )
        chunk["embedding"] = response.data[0].embedding
    return chunks

def get_collection():
    # embedding_function=None: we always supply OpenAI (1536-dim) vectors ourselves, so Chroma
    # must never fall back to its default 384-dim model (that caused a dimension mismatch before)
    return client.get_or_create_collection(
        "policies",
        embedding_function=None,
        metadata={"hnsw:space": "cosine"},
    )

def store_chunks_to_vector(chunks: list[dict]) -> None:
    # store chunk into chromadb collection with name "policies"
    collection = get_collection()
    # pass our OpenAI embeddings explicitly; otherwise Chroma embeds with its default 384-dim model
    collection.upsert(
        documents=[c["text"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[c["id"] for c in chunks],
    )

def run_rag_pipeline():
    # read file content from FILE_PATH
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_document(FILE_PATH, text)
    embeded_chunks = embed_chunks(chunks)
    store_chunks_to_vector(embeded_chunks)

def find_relevant_chunks(query: str, top_k: int = 5) -> list[dict]:
    # convert query to embedding
    # fire query on vector to find top K chunks
    query_embedding = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    chunks = []
    for i, ids in enumerate(results["ids"]):
        for j, chunk_id in enumerate(ids):
            chunks.append({
                "id": chunk_id,
                "text": results["documents"][i][j],
                "metadata": results["metadatas"][i][j],
            })
    return chunks

if __name__ == "__main__":
    # run_rag_pipeline()
    query = "How long I can keep my laptop after I left company"
    relevant_chunks = find_relevant_chunks(query)
    print(f"Relevant chunks for query: {query}, found {len(relevant_chunks)} chunks.")
    for chunk in relevant_chunks:
        print(chunk)