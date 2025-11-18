import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_utils import fetch_content

st.title("📚 Analysis History")

df = fetch_content()

if df is None or df.empty:
    st.info("No analyses yet.")
else:
    st.dataframe(df, use_container_width=True)

    search = st.text_input("Search text or strategy")

    if search.strip():
        mask = df.apply(lambda row: search.lower() in row.to_string().lower(), axis=1)
        filtered_df = df[mask]
        st.write(f"Found {len(filtered_df)} matching results")
        st.dataframe(filtered_df, use_container_width=True)
