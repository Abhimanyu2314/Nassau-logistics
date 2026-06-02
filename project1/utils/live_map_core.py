
import streamlit as st
import pandas as pd
import numpy as np

FAST_PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": True}

@st.cache_data(show_spinner=False, ttl=3600)
def live_map_data(seed=1010):
    rng = np.random.default_rng(seed)
    hubs = {
        "New York Hub": (40.7128, -74.0060),
        "Atlanta Hub": (33.7490, -84.3880),
        "Dallas Hub": (32.7767, -96.7970),
        "Denver Hub": (39.7392, -104.9903),
        "Los Angeles Hub": (34.0522, -118.2437),
        "Seattle Hub": (47.6062, -122.3321),
        "Chicago Hub": (41.8781, -87.6298),
        "Miami Hub": (25.7617, -80.1918),
    }
    names = list(hubs.keys())
    rows = []
    for i in range(42):
        src = rng.choice(names)
        dst = rng.choice([n for n in names if n != src])
        risk = float(np.clip(rng.normal(48, 22), 5, 98))
        volume = int(rng.integers(30, 520))
        eta = float(np.clip(rng.normal(3.2, 1.1), 0.8, 8))
        delay = float(np.clip(rng.normal(14, 12), 0, 75))
        rows.append({
            "Route_ID": f"NX-{1000+i}",
            "Origin": src,
            "Destination": dst,
            "Origin_Lat": hubs[src][0],
            "Origin_Lon": hubs[src][1],
            "Dest_Lat": hubs[dst][0],
            "Dest_Lon": hubs[dst][1],
            "Risk": risk,
            "Volume": volume,
            "ETA": eta,
            "Delay": delay,
            "Status": "Critical" if risk >= 70 else "Watch" if risk >= 45 else "Stable"
        })
    return pd.DataFrame(rows), hubs
