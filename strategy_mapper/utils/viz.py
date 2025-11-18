import pickle
import numpy as np
import pandas as pd
import altair as alt
from sklearn.decomposition import PCA
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_utils import connect

def radar_chart(similarity_dict, title="Strategy Alignment Radar"):
    """
    Creates a radar chart showing similarity scores across strategies.
    """
    df = pd.DataFrame({
        "strategy": list(similarity_dict.keys()),
        "score": list(similarity_dict.values())
    })
    df["angle"] = np.linspace(0, 2*np.pi, len(df), endpoint=False)
    df["cos"] = np.cos(df["angle"]) * df["score"]
    df["sin"] = np.sin(df["angle"]) * df["score"]

    chart = alt.Chart(df).mark_line(point=True).encode(
        x="cos:Q",
        y="sin:Q",
        tooltip=["strategy", "score"]
    ).properties(
        title=title,
        width=400,
        height=400
    )

    return chart

def pca_semantic_map():
    """
    Creates a PCA semantic map of all chunk embeddings.
    """
    conn = connect()
    cur = conn.cursor()

    # Load chunks with embeddings
    cur.execute("SELECT chunk_text, best_match, embedding FROM chunks")
    rows = cur.fetchall()
    conn.close()

    if len(rows) < 2:
        return None

    texts = [r[0][:50] + "..." if len(r[0]) > 50 else r[0] for r in rows]
    labels = [r[1] for r in rows]
    vectors = np.array([pickle.loads(r[2]) for r in rows])

    pca = PCA(n_components=2)
    reduced = pca.fit_transform(vectors)

    df = pd.DataFrame({
        "x": reduced[:, 0],
        "y": reduced[:, 1],
        "label": labels,
        "text": texts
    })

    chart = alt.Chart(df).mark_circle(size=100, opacity=0.7).encode(
        x="x:Q",
        y="y:Q",
        color="label:N",
        tooltip=["label", "text"]
    ).properties(width=800, height=500, title="Semantic Map (PCA)")

    return chart

def heatmap(similarity_matrix, chunk_labels, strategy_labels):
    """
    Creates a heatmap showing alignment between chunks and strategies.
    """
    df = pd.DataFrame(similarity_matrix, columns=strategy_labels)
    df["chunk"] = chunk_labels
    df = df.melt(id_vars=["chunk"], var_name="strategy", value_name="score")

    chart = alt.Chart(df).mark_rect().encode(
        x="strategy:N",
        y="chunk:N",
        color="score:Q",
        tooltip=["chunk", "strategy", "score"]
    ).properties(
        width=700,
        height=500,
        title="Alignment Heatmap"
    )

    return chart
