import json
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
# 1) Load JSON
with open("shl_product_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2) Convert each item into one embedding text
def build_text(item):
    parts = [
        f"Name: {item.get('name', '')}",
        f"Description: {item.get('description', '')}",
        f"Job levels: {', '.join(item.get('job_levels', []))}",
        f"Languages: {', '.join(item.get('languages', []))}",
        f"Duration: {item.get('duration', '')}",
        f"Remote: {item.get('remote', '')}",
        f"Adaptive: {item.get('adaptive', '')}",
        f"Category keys: {', '.join(item.get('keys', []))}",
    ]
    return " | ".join(parts)

texts = [build_text(item) for item in data]

# 3) Embed
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True
).astype("float32")

# 4) Build FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)   # cosine similarity because embeddings are normalized
index.add(embeddings)

# 5) Save index + metadata
faiss.write_index(index, "shl_catalog.faiss")
with open("shl_catalog_meta.pkl", "wb") as f:
    pickle.dump(data, f)