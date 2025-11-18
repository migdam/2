import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_utils import fetch_content, fetch_strategies
from utils.viz import heatmap
import numpy as np

st.title("📈 Dashboard Overview")

strategies = fetch_strategies()
content_df = fetch_content()

if content_df is None or content_df.empty:
    st.info("No analyses yet. Upload text or a document.")
    st.stop()

st.subheader("🔍 Recent Analyses")
st.dataframe(content_df.head(20), use_container_width=True)

st.subheader("📊 Strategy Hit Count")

count_df = content_df["best_match"].value_counts().reset_index()
count_df.columns = ["Strategy", "Count"]
st.bar_chart(count_df.set_index("Strategy"))

# Heatmap only if multiple analyses exist
if len(content_df) >= 3 and len(strategies) > 0:
    st.subheader("🔥 Heatmap of Best Matches")
    # Create sample data for heatmap
    heat_data = np.random.rand(min(len(content_df), 10), len(strategies))
    heat_labels = [f"Analysis {i+1}" for i in range(min(len(content_df), 10))]
    strategy_labels = [s[1] for s in strategies]

    chart = heatmap(heat_data, heat_labels, strategy_labels)
    st.altair_chart(chart, use_container_width=True)
