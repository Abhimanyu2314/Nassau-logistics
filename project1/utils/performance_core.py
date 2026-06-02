
import streamlit as st
import pandas as pd
import numpy as np

FAST_PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": False}

@st.cache_data(show_spinner=False, ttl=3600)
def generate_ops_data(seed=208, n=760):
    rng = np.random.default_rng(seed)
    hubs = ["Atlantic", "Gulf", "Interior", "Pacific"]
    modes = ["Standard", "Second Class", "First Class", "Same Day"]
    states = ["California","New York","Texas","Florida","Georgia","Arizona","Washington","Ohio","Colorado","Virginia","Kansas","Alabama","Louisiana","Maryland"]
    routes = ["LA-Dallas","NY-Chicago","Miami-Atlanta","Seattle-Denver","Houston-Phoenix","Boston-NYC","Dallas-Orlando","Denver-LA"]
    return pd.DataFrame({
        "Hub": rng.choice(hubs, n),
        "Mode": rng.choice(modes, n),
        "State": rng.choice(states, n),
        "Route": rng.choice(routes, n),
        "AI_Risk": np.clip(rng.normal(41, 18, n), 0, 100),
        "Delay": np.clip(rng.normal(16, 10, n), 0, 100),
        "Profit": rng.normal(2300, 520, n),
        "Volume": rng.integers(8, 280, n),
        "ETA": np.clip(rng.normal(3.5, 1.2, n), 1, 10),
        "SLA": np.clip(rng.normal(91, 5, n), 70, 99.8)
    })

def inject_speed_css():
    st.markdown("""
    <style>
    [data-testid="stSpinner"]{display:none!important}
    .stProgress > div > div > div > div{background-color:#2df5c4!important}
    section[data-testid="stSidebar"] *{transition:all .16s ease!important}
    iframe{border-radius:18px!important}
    </style>
    """, unsafe_allow_html=True)
