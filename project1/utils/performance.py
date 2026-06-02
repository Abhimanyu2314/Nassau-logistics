
import streamlit as st
import pandas as pd

@st.cache_data(show_spinner=False, ttl=3600)
def cached_dataframe(path: str):
    return pd.read_csv(path)

def fast_plotly_config():
    return {
        "displayModeBar": False,
        "responsive": True,
        "staticPlot": False,
        "scrollZoom": False,
    }

def page_ready_banner(label="Optimized page loaded"):
    st.success(f"⚡ {label} with caching enabled")
