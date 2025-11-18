import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_utils import fetch_content

st.title("⏳ Strategy Alignment Timeline")

st.markdown("""
View how your strategy alignments have evolved over time.
This helps identify trends and patterns in your strategic focus.
""")

df = fetch_content()

if df is None or df.empty:
    st.info("No analysis data available. Analyze some text or upload documents first.")
    st.stop()

# Convert created_at to datetime
df['created_at'] = pd.to_datetime(df['created_at'])

# Group by date and strategy
timeline = df.groupby([df['created_at'].dt.date, 'best_match']).size().reset_index(name='count')
timeline.columns = ['date', 'strategy', 'count']

st.subheader("📊 Analysis Count Over Time")

# Pivot for line chart
pivot_data = timeline.pivot(index='date', columns='strategy', values='count').fillna(0)
st.line_chart(pivot_data)

st.subheader("📋 Detailed Timeline Data")
st.dataframe(timeline.sort_values('date', ascending=False), use_container_width=True)
