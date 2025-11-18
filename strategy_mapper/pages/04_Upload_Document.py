import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_loader import load_text_from_file
from utils.chunker import agentic_chunk
from ai.embeddings import get_embedding
from ai.scorer import compute_similarity, best_match
from ai.reasoning import explain_alignment
from db.db_utils import fetch_strategies, insert_content, insert_chunk

st.title("📄 Upload Document")

strategies = fetch_strategies()

if not strategies:
    st.warning("No strategies defined. Please add strategies first.")
    st.stop()

uploaded = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])

if uploaded:
    with open("temp_upload", "wb") as f:
        f.write(uploaded.read())

    st.success("File uploaded. Processing...")

    try:
        text = load_text_from_file("temp_upload")
        chunks = agentic_chunk(text, mode="auto")

        st.write(f"Document split into **{len(chunks)} chunks**.")

        strategies_dicts = [
            {"id": id_, "name": n, "description": d, "embedding": e}
            for id_, n, d, e in strategies
        ]

        overall_matches = []

        content_id = insert_content(f"Uploaded: {uploaded.name}", None, None)

        progress_bar = st.progress(0)

        for i, ch in enumerate(chunks):
            st.write(f"### Chunk {i+1}")
            st.write(ch[:500] + "..." if len(ch) > 500 else ch)

            emb = get_embedding(ch)
            sims = compute_similarity(emb, strategies_dicts)
            top_name, top_score = best_match(sims)
            explanation = explain_alignment(ch, top_name, top_score)

            overall_matches.append(top_name)

            insert_chunk(content_id, ch, top_name, top_score, explanation, emb)

            st.info(f"Best: **{top_name}** ({top_score:.3f})")
            st.caption(explanation)

            progress_bar.progress((i + 1) / len(chunks))

        st.success("Document fully analyzed!")

        # Clean up temp file
        if os.path.exists("temp_upload"):
            os.remove("temp_upload")

    except Exception as e:
        st.error(f"Error processing document: {str(e)}")
        if os.path.exists("temp_upload"):
            os.remove("temp_upload")
