# scripts/load_vectorstore.py

import json5
import pickle
from pathlib import Path

import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "app" / "data" / "cleaned_shl_catalog.json"

VECTORSTORE_DIR = BASE_DIR / "app" / "vectorstore"

FAISS_PATH = VECTORSTORE_DIR / "shl_catalog.faiss"

VECTORIZER_PATH = VECTORSTORE_DIR / "tfidf_vectorizer.pkl"

METADATA_PATH = VECTORSTORE_DIR / "metadata.pkl"


# =========================================================
# LOAD DATASET
# =========================================================

def load_dataset():

    print(f"\nLoading dataset from:\n{DATA_PATH}\n")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json5.load(f)

    print(f"Loaded {len(data)} assessments.\n")

    return data


# =========================================================
# BUILD SEMANTIC TEXT
# =========================================================

def build_embedding_text(item):

    return f"""
    Assessment Name: {item.get("name", "")}

    Description:
    {item.get("description", "")}

    Job Levels:
    {", ".join(item.get("job_levels", []))}

    Languages:
    {", ".join(item.get("languages", []))}

    Duration:
    {item.get("duration", "")}

    Adaptive:
    {item.get("adaptive", "")}

    Remote:
    {item.get("remote", "")}

    Categories:
    {", ".join(item.get("keys", []))}
    """.strip()


# =========================================================
# PREPARE TEXTS
# =========================================================

def prepare_texts(data):

    print("Preparing semantic texts...\n")

    texts = [build_embedding_text(item) for item in data]

    print(f"Prepared {len(texts)} texts.\n")

    return texts


# =========================================================
# CREATE TF-IDF EMBEDDINGS
# =========================================================

def create_embeddings(texts):

    print("Creating TF-IDF vectors...\n")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    vectors = vectorizer.fit_transform(texts)

    embeddings = vectors.toarray().astype("float32")

    # Normalize vectors
    faiss.normalize_L2(embeddings)

    print("TF-IDF vectors created successfully.")
    print(f"Embedding shape: {embeddings.shape}\n")

    return embeddings, vectorizer


# =========================================================
# CREATE FAISS INDEX
# =========================================================

def create_faiss_index(embeddings):

    print("Creating FAISS index...\n")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print("FAISS index created successfully.")
    print(f"Indexed vectors: {index.ntotal}\n")

    return index


# =========================================================
# SAVE VECTORSTORE
# =========================================================

def save_vectorstore(index, vectorizer, metadata):

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    print("Saving FAISS index...\n")

    faiss.write_index(index, str(FAISS_PATH))

    print("Saving TF-IDF vectorizer...\n")

    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("Saving metadata...\n")

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("Vectorstore saved successfully.\n")


# =========================================================
# MAIN PIPELINE
# =========================================================

def main():

    data = load_dataset()

    texts = prepare_texts(data)

    embeddings, vectorizer = create_embeddings(texts)

    index = create_faiss_index(embeddings)

    save_vectorstore(index, vectorizer, data)

    print("=" * 60)
    print("VECTORSTORE CREATION COMPLETED SUCCESSFULLY")
    print("=" * 60)


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()