import streamlit as st
import os

st.set_page_config(
    page_title="Strategy Mapper",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Strategy Mapper")

st.markdown("""
Welcome to the **Strategy Alignment Analyzer**.

Use the navigation menu on the left to:
- Manage strategic pillars
- Analyze text
- Upload documents
- Explore semantic maps
- Review history
""")

# Ensure DB exists
if not os.path.exists("strategy_mapper.db"):
    st.warning("⚠️ Database not initialized. Run: `python db/init_db.py` first.")
else:
    st.success("Database connected ✓")
