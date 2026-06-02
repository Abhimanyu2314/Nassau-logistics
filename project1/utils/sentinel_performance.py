
import streamlit as st
FAST_PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": False}
def enable_fast_mode():
    st.session_state.setdefault("fast_mode", True)
    return st.session_state["fast_mode"]
