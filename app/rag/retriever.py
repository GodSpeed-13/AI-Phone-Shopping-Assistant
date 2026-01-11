import json
import faiss
import numpy as np
from app.rag.embedder import embed

with open("app/data/phones.json") as f:
    PHONES = json.load(f)

index = faiss.read_index("app/data/faiss.index")

def retrieve_phones(budget=None, brands=None, use_cases=None, k=3):
    results = PHONES

    # Normalize brand names
    if brands:
        brands = [b.lower() for b in brands]
        results = [
            p for p in results
            if p["brand"].lower() in brands
        ]

    # Apply budget filter
    if budget:
        results = [
            p for p in results
            if p["price"] <= budget
        ]

    # If brands were specified, DO NOT fallback
    if brands:
        return results[:k]

    # ---------- Semantic fallback only if NO brand constraint ----------
    if not results:
        query = " ".join(use_cases) if use_cases else "best phone"
        query_embedding = embed([query])
        scores, ids = index.search(query_embedding, k)
        results = [PHONES[i] for i in ids[0]]

    return results[:k]
