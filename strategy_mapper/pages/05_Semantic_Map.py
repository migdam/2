import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.viz import pca_semantic_map

st.title("🗺️ Semantic Map (PCA)")

st.markdown("""
This visualization shows how your analyzed content clusters semantically.
Each point represents a chunk of text, colored by its best-matching strategy.
""")

chart = pca_semantic_map()

if chart is None:
    st.info("Need at least 2 chunks to generate PCA map. Analyze some text or upload a document first.")
else:
    st.altair_chart(chart, use_container_width=True)
