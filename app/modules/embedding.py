import json
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
# 1) load json
with open("shl_product_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# embedding
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


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True
).astype("float32")

# FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)   # cosine similarity because embeddings are normalized
index.add(embeddings)


faiss.write_index(index, "shl_catalog.faiss")
with open("shl_catalog_meta.pkl", "wb") as f:
    pickle.dump(data, f)