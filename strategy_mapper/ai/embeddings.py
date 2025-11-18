import os
import numpy as np
import pickle
import hashlib
from openai import OpenAI

client = OpenAI()

CACHE_PATH = "embedding_cache.pkl"

# -------------------------------------------------
# Load / save embedding cache
# -------------------------------------------------
def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(cache, f)

# -------------------------------------------------
# Embedding function with caching
# -------------------------------------------------
def get_embedding(text: str):
    """
    Compute embedding via OpenAI with caching.
    """
    cache = load_cache()
    key = hashlib.sha256(text.encode()).hexdigest()

    if key in cache:
        return cache[key]

    # Primary high-quality embedding
    model = "text-embedding-3-large"

    try:
        resp = client.embeddings.create(model=model, input=text)
        vec = np.array(resp.data[0].embedding, dtype=np.float32)

    except Exception:
        # Fallback model (lighter, cheaper)
        resp = client.embeddings.create(model="text-embedding-3-small", input=text)
        vec = np.array(resp.data[0].embedding, dtype=np.float32)

    cache[key] = vec
    save_cache(cache)
    return vec
