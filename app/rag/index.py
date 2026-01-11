import json
import faiss
import numpy as np
from embedder import embed

with open("app/data/phones.json") as f:
    phones = json.load(f)

documents = [
    (
        f"{p['brand']} {p['model']} is priced at ₹{p['price']}. "
        f"It features a {p['display']} display, powered by the {p['processor']} processor. "
        f"The phone offers a {p['camera']} camera setup and a {p['battery']} battery "
        f"with {p['charging']} charging support. "
        f"Key features include {', '.join(p['features'])}."
    )
    for p in phones
]

embeddings = embed(documents)
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "app/data/faiss.index")
