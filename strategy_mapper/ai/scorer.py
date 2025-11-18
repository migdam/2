import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(content_vec, strategies):
    """
    strategies: list of dicts with keys: id, name, description, embedding
    Returns sorted list of {"strategy": name, "score": float}
    """
    results = []
    for s in strategies:
        score = float(cosine_similarity([content_vec], [s["embedding"]])[0][0])
        results.append({"strategy": s["name"], "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def best_match(similarity_list):
    """
    Given output of compute_similarity → return best match tuple.
    """
    top = similarity_list[0]
    return top["strategy"], top["score"]
