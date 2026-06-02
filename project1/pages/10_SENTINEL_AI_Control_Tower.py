
import streamlit as st
from utils.common import setup_page
import pandas as pd
import numpy as np
import plotly.graph_objects as go

setup_page("SENTINEL AI Control Tower")

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 12% 10%,rgba(45,245,196,.14),transparent 25%),radial-gradient(circle at 84% 14%,rgba(86,166,255,.12),transparent 26%),linear-gradient(135deg,#050911,#08101b 52%,#050b12)!important}
.block-container{padding-top:1rem!important;max-width:1620px!important}
.sentinel{border:1px solid rgba(45,245,196,.30);border-radius:32px;padding:26px;background:linear-gradient(145deg,rgba(10,19,32,.94),rgba(9,31,35,.72));box-shadow:0 24px 90px rgba(0,0,0,.42),inset 0 0 80px rgba(45,245,196,.055);position:relative;overflow:hidden}
.sentinel:before{content:"";position:absolute;inset:-2px;background:linear-gradient(115deg,transparent,rgba(45,245,196,.18),transparent);transform:translateX(-80%);animation:scan 4.8s linear infinite}
@keyframes scan{100%{transform:translateX(80%)}} @keyframes pulse{50%{opacity:.45;transform:scale(.75)}}
.top{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;position:relative;z-index:1;flex-wrap:wrap}
.kicker{color:#2df5c4;font-size:12px;font-weight:950;letter-spacing:.18em}
.top h1{font-size:56px!important;line-height:1!important;letter-spacing:-.055em;margin:6px 0 8px 0!important;color:#f3fbff!important}
.top p{color:#a7b8cb!important;font-size:17px!important;margin:0!important;max-width:920px}
.live{border:1px solid rgba(45,245,196,.38);background:rgba(45,245,196,.08);color:#2df5c4;border-radius:999px;padding:11px 15px;font-weight:950;display:flex;align-items:center;gap:9px}
.live span{width:10px;height:10px;border-radius:50%;background:#2df5c4;box-shadow:0 0 20px #2df5c4;animation:pulse 1.2s infinite}
.metric-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:20px;position:relative;z-index:1}
.metric{border:1px solid rgba(86,166,255,.22);border-radius:22px;padding:16px;background:linear-gradient(145deg,rgba(12,23,38,.9),rgba(8,14,24,.78));box-shadow:0 16px 45px rgba(0,0,0,.28);transition:.18s ease}
.metric:hover{transform:translateY(-3px);border-color:rgba(45,245,196,.50);box-shadow:0 0 36px rgba(45,245,196,.11)}
.metric small{display:block;color:#94a8bb;text-transform:uppercase;letter-spacing:.11em;font-size:10px;font-weight:950}
.metric b{display:block;color:#fff;font-size:27px;line-height:1.2;margin-top:5px}
.metric em{display:block;color:#2df5c4;font-style:normal;font-size:12px;font-weight:800;margin-top:3px}
.panel{border:1px solid rgba(86,166,255,.22);border-radius:25px;padding:16px;background:rgba(9,17,28,.74);box-shadow:0 18px 60px rgba(0,0,0,.28)}
.panel h3{margin:0 0 12px 0!important;color:#f4fbff!important;font-size:19px!important}
.action-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.action{border:1px solid rgba(45,245,196,.24);background:rgba(45,245,196,.075);color:#eafff9;border-radius:18px;padding:14px;font-weight:950;text-align:center;transition:.18s ease}
.action:hover{transform:scale(1.02);box-shadow:0 0 28px rgba(45,245,196,.13)}
.stream{display:flex;gap:12px;align-items:center;padding:12px;border-radius:16px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.075);margin-bottom:9px}
.stream span{width:10px;height:10px;border-radius:50%;box-shadow:0 0 18px currentColor;background:currentColor;color:#2df5c4}
.stream.warn span{color:#ffbf4d}.stream.crit span{color:#ff3860}
.stream b{color:#fff}.stream small{display:block;color:#9fb3c8;margin-top:2px}
.command{margin:16px 0;display:grid;grid-template-columns:1.8fr 1fr;gap:12px}
.cmd{border:1px solid rgba(45,245,196,.30);border-radius:22px;padding:16px 18px;background:linear-gradient(135deg,rgba(45,245,196,.08),rgba(86,166,255,.045));color:#dffcf6;font-weight:900}
.cmd small{display:block;color:#99acbd;font-weight:800;margin-top:4px}
.footer{margin-top:16px;border:1px solid rgba(45,245,196,.20);background:rgba(45,245,196,.055);border-radius:18px;padding:14px;text-align:center;color:#2df5c4;font-weight:950}
@media(max-width:1000px){.metric-grid{grid-template-columns:1fr 1fr}.command{grid-template-columns:1fr}}
@media(max-width:650px){.metric-grid,.action-grid{grid-template-columns:1fr}.top h1{font-size:38px!important}}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False, ttl=1800)
def sentinel_data(seed=42):
    rng = np.random.default_rng(seed)
    hubs = ["Atlantic", "Gulf", "Interior", "Pacific"]
    modes = ["Standard", "Second Class", "First Class", "Same Day"]
    states = ["California","New York","Texas","Florida","Georgia","Arizona","Washington","Ohio","Colorado","Virginia","Kansas","Alabama"]
    n = 720
    return pd.DataFrame({
        "Hub": rng.choice(hubs, n), "Mode": rng.choice(modes, n), "State": rng.choice(states, n),
        "AI_Risk": np.clip(rng.normal(43, 19, n), 0, 100),
        "Delay": np.clip(rng.normal(18, 11, n), 0, 100),
        "Profit": rng.normal(2100, 530, n), "Volume": rng.integers(8, 260, n)
    })

df = sentinel_data()
total_volume = int(df["Volume"].sum())
risk = df["AI_Risk"].mean()
delay = df["Delay"].mean()
profit = df["Profit"].sum()
modes = df["Mode"].nunique()

st.markdown(f"""
<div class="sentinel"><div class="top"><div><div class="kicker">TITAN ENTERPRISE • PHASE 6 SENTINEL</div>
<h1>SENTINEL AI Control Tower</h1>
<p>Next-level fast command layer with lazy analytics, command shortcuts, risk stream, instant executive charts, and stabilized Plotly rendering.</p></div>
<div class="live"><span></span> SENTINEL ONLINE</div></div>
<div class="metric-grid">
<div class="metric"><small>Shipment Volume</small><b>{total_volume:,}</b><em>network flow</em></div>
<div class="metric"><small>AI Risk</small><b>{risk:.1f}%</b><em>predictive index</em></div>
<div class="metric"><small>Delay Pressure</small><b>{delay:.1f}%</b><em>SLA radar</em></div>
<div class="metric"><small>Profit Signal</small><b>${profit/1_000_000:.2f}M</b><em>financial pulse</em></div>
<div class="metric"><small>Ship Modes</small><b>{modes}</b><em>active channels</em></div>
</div></div>
<div class="command"><div class="cmd">⌘ Sentinel Command: Analyze high-risk hubs and rebalance shipments <small>No heavy map tiles. No blocking loaders. No invalid Plotly colorbar properties.</small></div>
<div class="cmd">⚡ Load Target: under 1.5 seconds <small>Uses cached synthetic intelligence layer.</small></div></div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.45, 1])
with c1:
    st.markdown('<div class="panel"><h3>🧬 Neural Hub Risk Matrix</h3>', unsafe_allow_html=True)
    matrix = df.groupby(["Hub", "Mode"], observed=True).agg(Risk=("AI_Risk","mean")).reset_index()
    pivot = matrix.pivot(index="Hub", columns="Mode", values="Risk").fillna(0)
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=[[0,"#053b75"],[.45,"#2df5c4"],[.72,"#ffbf4d"],[1,"#ff3860"]],
        colorbar=dict(title=dict(text="Risk", font=dict(color="#dcecff")), tickfont=dict(color="#dcecff")),
        hovertemplate="<b>%{y}</b><br>Mode: %{x}<br>Risk: %{z:.1f}%<extra></extra>"
    ))
    fig.update_layout(template="plotly_dark", height=390, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    high = df.groupby("State").agg(Risk=("AI_Risk","mean"), Volume=("Volume","sum"), Delay=("Delay","mean")).sort_values("Risk", ascending=False).head(6)
    items = ""
    for state, row in high.iterrows():
        cls = "crit" if row["Risk"] > 55 else "warn"
        items += f'<div class="stream {cls}"><span></span><div><b>{state}</b><small>{row["Risk"]:.1f}% risk • {int(row["Volume"]):,} volume • {row["Delay"]:.1f}% delay</small></div></div>'
    st.markdown(f'<div class="panel"><h3>🚨 Sentinel Escalation Stream</h3>{items}</div>', unsafe_allow_html=True)

c3, c4 = st.columns([1.25, 1])
with c3:
    st.markdown('<div class="panel"><h3>📊 Predictive Operations Pulse</h3>', unsafe_allow_html=True)
    t = np.arange(1, 25); rng = np.random.default_rng(7)
    y1 = 88 + np.cumsum(rng.normal(0, .9, 24)); y2 = 42 + np.cumsum(rng.normal(0, 1.3, 24))
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t, y=y1, mode="lines+markers", name="Delivery Health", line=dict(color="#2df5c4", width=3)))
    fig2.add_trace(go.Scatter(x=t, y=y2, mode="lines+markers", name="Risk Load", line=dict(color="#ffbf4d", width=3)))
    fig2.update_layout(template="plotly_dark", height=330, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h"))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown("""<div class="panel"><h3>⚙️ Sentinel Quick Actions</h3>
    <div class="action-grid"><div class="action">AI Rebalance</div><div class="action">Delay Scan</div><div class="action">Route Pulse</div><div class="action">Export Report</div><div class="action">Fleet Watch</div><div class="action">Risk Forecast</div></div></div>
    <div class="footer">✓ Phase 6 ready • ✓ Faster pages • ✓ Fixed Plotly pattern • ✓ Executive command experience</div>""", unsafe_allow_html=True)
