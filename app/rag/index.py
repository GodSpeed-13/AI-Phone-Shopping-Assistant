import json
import faiss
import numpy as np
from embedder import embed

with open("app/data/phones.json") as f:
    phones = json.load(f)

documents = [
    f"{p['brand']} {p['model']} priced at ₹{p['price']} with {p['camera']} camera, {p['battery']} battery."
    for p in phones
]

embeddings = embed(documents)
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "app/data/faiss.index")
