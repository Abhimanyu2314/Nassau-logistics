
import streamlit as st
import pandas as pd
import numpy as np

FAST_PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": False}

@st.cache_data(show_spinner=False, ttl=3600)
def premium_data(seed=909, n=950):
    rng = np.random.default_rng(seed)
    hubs = ["Atlantic", "Gulf", "Interior", "Pacific"]
    modes = ["Standard", "Second Class", "First Class", "Same Day"]
    states = ["California","New York","Texas","Florida","Georgia","Arizona","Washington","Ohio","Colorado","Virginia","Kansas","Alabama","Louisiana","Maryland","Connecticut","Rhode Island"]
    routes = ["LA → Dallas","NY → Chicago","Miami → Atlanta","Seattle → Denver","Houston → Phoenix","Boston → NYC","Dallas → Orlando","Denver → LA","Atlanta → Charlotte"]
    return pd.DataFrame({
        "Hub": rng.choice(hubs, n),
        "Mode": rng.choice(modes, n),
        "State": rng.choice(states, n),
        "Route": rng.choice(routes, n),
        "AI_Risk": np.clip(rng.normal(40, 18, n), 0, 100),
        "Delay": np.clip(rng.normal(15, 10, n), 0, 100),
        "Profit": rng.normal(2450, 540, n),
        "Volume": rng.integers(10, 320, n),
        "ETA": np.clip(rng.normal(3.4, 1.1, n), 1, 10),
        "SLA": np.clip(rng.normal(92, 4.8, n), 72, 99.9),
        "Capacity": np.clip(rng.normal(76, 12, n), 35, 99)
    })

def inject_premium_css():
    st.markdown("""
    <style>
    [data-testid="stSpinner"]{display:none!important}
    .stProgress > div > div > div > div{background-color:#2df5c4!important}
    section[data-testid="stSidebar"]{background:linear-gradient(180deg,#07111e,#050914)!important}
    section[data-testid="stSidebar"] *{transition:all .16s ease!important}
    iframe{border-radius:18px!important}
    </style>
    """, unsafe_allow_html=True)
