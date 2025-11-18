import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.embeddings import get_embedding
from db.db_utils import fetch_strategies, insert_strategy, delete_strategy

st.title("🧭 Strategy Manager")

st.subheader("Existing Strategies")
strategies = fetch_strategies()

for id_, name, desc, emb in strategies:
    with st.expander(f"{name}"):
        st.write(desc)
        if st.button(f"Delete '{name}'", key=f"del_{id_}"):
            delete_strategy(id_)
            st.rerun()

st.subheader("➕ Add New Strategy")

name = st.text_input("Strategy name")
desc = st.text_area("Description")

if st.button("Create Strategy"):
    if not name.strip() or not desc.strip():
        st.error("Both name and description required!")
    else:
        emb = get_embedding(desc)
        insert_strategy(name, desc, emb)
        st.success("Strategy added!")
        st.rerun()
