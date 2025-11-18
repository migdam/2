import numpy as np
import pandas as pd
import altair as alt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def cluster_strategies(strategies, k=3):
    """
    Cluster strategies based on semantic similarity.

    strategies = [(id, name, desc, emb)]
    Returns an Altair chart showing strategy clusters.
    """
    if len(strategies) < k:
        k = max(1, len(strategies))

    names = [s[1] for s in strategies]
    vecs = np.array([s[3] for s in strategies])

    # Apply PCA for visualization
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(vecs)

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = kmeans.fit_predict(vecs)

    df = pd.DataFrame({
        "strategy": names,
        "cluster": [f"Cluster {l+1}" for l in labels],
        "x": reduced[:, 0],
        "y": reduced[:, 1]
    })

    chart = alt.Chart(df).mark_circle(size=300).encode(
        x=alt.X("x:Q", title="PCA Component 1"),
        y=alt.Y("y:Q", title="PCA Component 2"),
        color=alt.Color("cluster:N", title="Cluster"),
        tooltip=["strategy", "cluster"]
    ).properties(
        width=600,
        height=400,
        title="Strategy Clusters (K-Means + PCA)"
    ).interactive()

    return chart
