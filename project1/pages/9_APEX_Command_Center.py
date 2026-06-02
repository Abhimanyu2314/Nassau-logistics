
import streamlit as st
from utils.common import setup_page
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import time

setup_page("APEX Command Center")

# ---------- Fast global styles ----------
st.markdown("""
<style>
:root{
  --bg:#070d14; --panel:rgba(14,24,38,.86); --line:rgba(45,245,196,.28);
  --green:#2df5c4; --blue:#56a6ff; --red:#ff3860; --yellow:#ffbf4d;
}
.stApp{
  background:
    radial-gradient(circle at 8% 12%, rgba(45,245,196,.12), transparent 24%),
    radial-gradient(circle at 88% 10%, rgba(86,166,255,.11), transparent 28%),
    linear-gradient(135deg,#060a10,#0a111d 55%,#071017)!important;
}
.block-container{padding-top:1.2rem!important; max-width:1600px!important}
.apex-hero{
  border:1px solid var(--line); border-radius:30px; padding:26px 28px; margin-bottom:18px;
  background:linear-gradient(135deg,rgba(12,22,35,.92),rgba(9,34,35,.75));
  box-shadow:0 20px 80px rgba(0,0,0,.38), inset 0 0 60px rgba(45,245,196,.05);
  position:relative; overflow:hidden;
}
.apex-hero:before{
  content:""; position:absolute; inset:-2px; pointer-events:none;
  background:linear-gradient(110deg,transparent,rgba(45,245,196,.18),transparent);
  transform:translateX(-80%); animation:scan 5s linear infinite;
}
@keyframes scan{to{transform:translateX(80%)}}
.kicker{color:var(--green);font-weight:900;letter-spacing:.16em;font-size:12px}
.apex-hero h1{font-size:54px; margin:.25rem 0!important; color:#f1fbff; letter-spacing:-.05em}
.apex-hero p{color:#a9bacb;font-size:17px;margin:0!important}
.status-pill{display:inline-flex;align-items:center;gap:9px;border:1px solid var(--line);padding:10px 14px;border-radius:999px;color:var(--green);background:rgba(45,245,196,.08);font-weight:900}
.status-dot{width:10px;height:10px;border-radius:50%;background:var(--green);box-shadow:0 0 18px var(--green);animation:pulse 1.25s infinite}
@keyframes pulse{50%{opacity:.45;transform:scale(.75)}}
.apex-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:16px 0}
.apex-card{
  background:linear-gradient(145deg,rgba(13,24,38,.9),rgba(9,16,27,.78));
  border:1px solid rgba(86,166,255,.22); border-radius:22px; padding:18px;
  box-shadow:0 16px 45px rgba(0,0,0,.26); transition:.2s ease;
}
.apex-card:hover{transform:translateY(-3px);border-color:rgba(45,245,196,.48);box-shadow:0 0 35px rgba(45,245,196,.10)}
.apex-card small{display:block;color:#97aabd;text-transform:uppercase;letter-spacing:.11em;font-size:11px;font-weight:900}
.apex-card b{display:block;color:#fff;font-size:30px;margin-top:5px}
.apex-card em{display:block;color:var(--green);font-style:normal;font-size:12px;margin-top:5px;font-weight:800}
.panel{
  border:1px solid rgba(86,166,255,.22); border-radius:24px; padding:16px;
  background:rgba(9,17,28,.76); box-shadow:0 18px 55px rgba(0,0,0,.25);
}
.panel h3{margin:0 0 10px 0!important;color:#f3fbff;font-size:19px}
.command-feed{display:flex;flex-direction:column;gap:10px}
.feed-item{display:flex;align-items:center;gap:12px;padding:13px;border-radius:16px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08)}
.feed-item span{width:11px;height:11px;border-radius:50%;background:var(--green);box-shadow:0 0 16px var(--green)}
.feed-item b{color:#fff}.feed-item small{display:block;color:#9fb3c8}
.quick-actions{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.quick-actions div{border:1px solid rgba(45,245,196,.25);background:rgba(45,245,196,.07);padding:14px;border-radius:18px;color:#dffcf6;font-weight:900;text-align:center}
.footer-strip{margin-top:16px;border:1px solid rgba(45,245,196,.18);border-radius:18px;padding:14px;text-align:center;color:var(--green);font-weight:900;background:rgba(45,245,196,.045)}
@media(max-width:950px){.apex-grid{grid-template-columns:1fr 1fr}.quick-actions{grid-template-columns:1fr}.apex-hero h1{font-size:38px}}
@media(max-width:600px){.apex-grid{grid-template-columns:1fr}}
</style>
""", unsafe_allow_html=True)

# ---------- Ultra-fast cached sample data ----------
@st.cache_data(show_spinner=False, ttl=3600)
def load_fast_data():
    np.random.seed(22)
    states = ["California","New York","Texas","Florida","Georgia","Arizona","Washington","Ohio","Colorado","Virginia","Kansas","Alabama"]
    routes = ["LA → Dallas","NY → Chicago","Miami → Atlanta","Seattle → Denver","Houston → Phoenix","Boston → NYC"]
    n = 650
    df = pd.DataFrame({
        "state": np.random.choice(states, n),
        "route": np.random.choice(routes, n),
        "risk": np.random.beta(2.2, 3.6, n) * 100,
        "shipments": np.random.randint(20, 240, n),
        "delay": np.random.rand(n) * 42,
        "profit": np.random.normal(1850, 420, n)
    })
    return df

df = load_fast_data()

# ---------- Header ----------
st.markdown("""
<div class="apex-hero">
  <div style="display:flex;justify-content:space-between;gap:16px;align-items:flex-start;position:relative;z-index:1;flex-wrap:wrap">
    <div>
      <div class="kicker">TITAN ENTERPRISE • PHASE 5 APEX</div>
      <h1>APEX AI Command Center</h1>
      <p>Ultra-fast logistics intelligence layer with cached analytics, lightweight visualizations, fixed Plotly errors, and responsive enterprise UX.</p>
    </div>
    <div class="status-pill"><span class="status-dot"></span> OPTIMIZED LIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- KPIs ----------
total_ship = int(df["shipments"].sum())
avg_risk = df["risk"].mean()
delay = df["delay"].mean()
profit = df["profit"].sum()

st.markdown(f"""
<div class="apex-grid">
  <div class="apex-card"><small>Total Shipment Flow</small><b>{total_ship:,}</b><em>cached command layer</em></div>
  <div class="apex-card"><small>AI Risk Index</small><b>{avg_risk:.1f}%</b><em>predictive risk model</em></div>
  <div class="apex-card"><small>Delay Pressure</small><b>{delay:.1f}%</b><em>SLA watch active</em></div>
  <div class="apex-card"><small>Profit Signal</small><b>${profit/1_000_000:.2f}M</b><em>executive financial pulse</em></div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.5, 1])

with c1:
    st.markdown('<div class="panel"><h3>⚡ Lightweight AI Risk Heatmap</h3>', unsafe_allow_html=True)
    heat = df.groupby(["state","route"], observed=True).agg(risk=("risk","mean"), shipments=("shipments","sum")).reset_index()
    pivot = heat.pivot(index="state", columns="route", values="risk").fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=[[0,"#003b73"],[.45,"#2df5c4"],[.72,"#ffbf4d"],[1,"#ff3860"]],
        colorbar=dict(title=dict(text="AI Risk", font=dict(color="#dcecff")), tickfont=dict(color="#dcecff")),
        hovertemplate="<b>%{y}</b><br>Route: %{x}<br>AI Risk: %{z:.1f}%<extra></extra>"
    ))
    fig.update_layout(
        template="plotly_dark",
        height=430,
        margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(color="#dcecff")),
        yaxis=dict(tickfont=dict(color="#dcecff"))
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    top = df.groupby("state").agg(risk=("risk","mean"), shipments=("shipments","sum")).sort_values("risk", ascending=False).head(6)
    items = ""
    for state, row in top.iterrows():
        zone = "CRITICAL" if row["risk"] > 55 else "WATCH"
        items += f'<div class="feed-item"><span></span><div><b>{state}</b><small>{zone} • {row["risk"]:.1f}% risk • {int(row["shipments"]):,} shipments</small></div></div>'
    st.markdown(f"""
    <div class="panel">
      <h3>🧠 Neural Escalation Feed</h3>
      <div class="command-feed">{items}</div>
    </div>
    """, unsafe_allow_html=True)

c3, c4 = st.columns([1,1])
with c3:
    st.markdown('<div class="panel"><h3>📈 Predictive Delivery Trend</h3>', unsafe_allow_html=True)
    x = list(range(1, 25))
    y = np.cumsum(np.random.normal(0, 1.1, 24)) + 92
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(width=3, color="#2df5c4"), marker=dict(size=7)))
    fig2.update_layout(template="plotly_dark", height=300, margin=dict(l=10,r=10,t=5,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="panel">
      <h3>🚀 APEX Quick Actions</h3>
      <div class="quick-actions">
        <div>Optimize Routes</div>
        <div>Scan Delays</div>
        <div>Generate Report</div>
        <div>Risk Forecast</div>
        <div>Fleet Pulse</div>
        <div>Export Insights</div>
      </div>
    </div>
    <div class="footer-strip">✓ All heavy pages optimized with caching strategy • ✓ Plotly ColorBar error fixed pattern • ✓ Fast command center ready</div>
    """, unsafe_allow_html=True)
