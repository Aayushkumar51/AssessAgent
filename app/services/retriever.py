import pickle
from pathlib import Path

import faiss
import numpy as np


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

FAISS_PATH = VECTORSTORE_DIR / "shl_catalog.faiss"

VECTORIZER_PATH = VECTORSTORE_DIR / "tfidf_vectorizer.pkl"

METADATA_PATH = VECTORSTORE_DIR / "metadata.pkl"


# =========================================================
# LOAD VECTORSTORE
# =========================================================

print("\nLoading FAISS index...\n")

index = faiss.read_index(str(FAISS_PATH))

print("FAISS index loaded.\n")

print("Loading TF-IDF vectorizer...\n")

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

print("TF-IDF vectorizer loaded.\n")

print("Loading metadata...\n")

with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

print("Metadata loaded.\n")


# =========================================================
# SEARCH FUNCTION
# =========================================================

def search_assessments(query, top_k=5):

    print(f"\nSearching for:\n{query}\n")

    # Convert query → TF-IDF vector
    query_vector = vectorizer.transform([query])

    query_embedding = query_vector.toarray().astype("float32")

    # Normalize
    faiss.normalize_L2(query_embedding)

    # Search FAISS
    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        item = metadata[idx]

        results.append({
            "name": item.get("name"),
            "url": item.get("link"),
            "description": item.get("description"),
            "job_levels": item.get("job_levels"),
            "duration": item.get("duration"),
            "remote": item.get("remote"),
            "adaptive": item.get("adaptive"),
            "categories": item.get("keys"),
            "score": float(score)
        })

    return results


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    query = "Hiring a Java developer with stakeholder communication skills"

    results = search_assessments(query, top_k=5)

    print("\nTOP RESULTS:\n")

    for i, result in enumerate(results, start=1):

        print("=" * 60)

        print(f"Rank: {i}")

        print(f"Name: {result['name']}")

        print(f"Score: {result['score']:.4f}")

        print(f"Duration: {result['duration']}")

        print(f"Categories: {result['categories']}")

        print(f"URL: {result['url']}")

        print()