#!/usr/bin/env python3
"""
RAG Tutorial 07 — Parent-Document Retrieval
Minimal example: store small child chunks for retrieval, return larger parent context.
Run: pip install -r requirements.txt && python example.py
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Parent sections (e.g. full paragraphs); children are smaller pieces for precise match
PARENTS = [
    "RAG uses retrieval to find relevant documents. Then an LLM generates an answer using that context. This reduces hallucinations.",
    "Chunking splits documents into smaller pieces. Too small loses context; too large adds noise. Parent-document retrieval retrieves small chunks but returns the full parent section.",
]
CHILDREN = [
    "RAG uses retrieval to find relevant documents.",
    "Then an LLM generates an answer using that context.",
    "Chunking splits documents into smaller pieces.",
    "Parent-document retrieval retrieves small chunks but returns the full parent section.",
]
# child i maps to parent parent_ids[i]
PARENT_IDS = [0, 0, 1, 1]


def main():
    client = chromadb.Client(Settings(anonymized_telemetry=False))
    coll = client.get_or_create_collection("parent_doc_example")
    child_embeddings = model.encode(CHILDREN).tolist()
    coll.add(
        ids=[f"child_{i}" for i in range(len(CHILDREN))],
        embeddings=child_embeddings,
        documents=CHILDREN,
        metadatas=[{"parent_id": PARENT_IDS[i]} for i in range(len(CHILDREN))],
    )
    query = "What does the LLM do with the context?"
    results = coll.query(
        query_embeddings=model.encode([query]).tolist(),
        n_results=2,
        include=["documents", "metadatas"],
    )
    parent_indices = set()
    for meta in results["metadatas"][0]:
        parent_indices.add(meta["parent_id"])
    context = "\n\n".join(PARENTS[i] for i in sorted(parent_indices))
    print("Query:", query)
    print("Retrieved child chunks:", results["documents"][0])
    print("Expanded parent context:\n", context)
    print("\n→ LLM receives full parent sections instead of tiny fragments.")


if __name__ == "__main__":
    main()
