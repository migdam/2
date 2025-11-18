import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.embeddings import get_embedding
from ai.scorer import compute_similarity, best_match
from ai.reasoning import explain_alignment
from db.db_utils import fetch_strategies, insert_content, insert_chunk
from utils.viz import radar_chart

st.title("📝 Analyze Text")

strategies = fetch_strategies()

if not strategies:
    st.warning("No strategies defined. Please add strategies first.")
    st.stop()

text = st.text_area("Enter text to analyze:", height=250)

if st.button("Analyze"):
    if not text.strip():
        st.warning("Please enter text.")
        st.stop()

    with st.spinner("Analyzing..."):
        emb = get_embedding(text)
        strategies_dicts = [
            {"id": id_, "name": n, "description": d, "embedding": e}
            for id_, n, d, e in strategies
        ]

        sims = compute_similarity(emb, strategies_dicts)
        top_name, top_score = best_match(sims)

        explanation = explain_alignment(text, top_name, top_score)

        st.subheader("🏁 Result")
        st.success(f"Best match: **{top_name}** (score: {top_score:.3f})")
        st.info(explanation)

        # Save
        content_id = insert_content(text, top_name, top_score)
        insert_chunk(content_id, text, top_name, top_score, explanation, emb)

        st.subheader("📊 Full Similarity Scores")
        for item in sims:
            st.write(f"- {item['strategy']}: {item['score']:.3f}")

        # Radar chart
        st.subheader("🕸️ Radar Chart")
        sim_dict = {x['strategy']: x['score'] for x in sims}
        radar = radar_chart(sim_dict)
        st.altair_chart(radar, use_container_width=True)
