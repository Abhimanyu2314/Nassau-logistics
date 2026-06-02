
import streamlit as st
from utils.common import setup_page
import pandas as pd
import numpy as np
import plotly.graph_objects as go

setup_page("QUANTUM OPS Nexus")

st.markdown("""
<style>
.stApp{
  background:
    radial-gradient(circle at 15% 8%,rgba(45,245,196,.16),transparent 26%),
    radial-gradient(circle at 84% 18%,rgba(86,166,255,.14),transparent 28%),
    radial-gradient(circle at 50% 90%,rgba(172,80,255,.10),transparent 30%),
    linear-gradient(135deg,#040812,#07111c 55%,#050b12)!important;
}
.block-container{padding-top:1rem!important;max-width:1650px!important}
.quantum-hero{
  border:1px solid rgba(45,245,196,.32);
  border-radius:34px;
  padding:28px;
  background:
    linear-gradient(145deg,rgba(9,19,33,.96),rgba(8,37,39,.74)),
    repeating-linear-gradient(90deg,rgba(255,255,255,.03) 0 1px,transparent 1px 80px);
  box-shadow:0 25px 100px rgba(0,0,0,.48), inset 0 0 90px rgba(45,245,196,.055);
  position:relative;overflow:hidden;margin-bottom:16px;
}
.quantum-hero:before{
  content:"";position:absolute;inset:-3px;
  background:linear-gradient(115deg,transparent,rgba(45,245,196,.2),rgba(86,166,255,.12),transparent);
  transform:translateX(-88%);animation:scan 5s linear infinite;
}
@keyframes scan{100%{transform:translateX(88%)}} @keyframes pulse{50%{opacity:.45;transform:scale(.72)}}
.hero-top{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;flex-wrap:wrap;position:relative;z-index:1}
.kicker{color:#2df5c4;font-size:12px;font-weight:950;letter-spacing:.18em}
.hero-top h1{font-size:58px!important;line-height:.98!important;letter-spacing:-.06em;margin:7px 0 8px 0!important;color:#f3fbff!important}
.hero-top p{color:#a8bacb!important;font-size:17px!important;margin:0!important;max-width:980px}
.live{border:1px solid rgba(45,245,196,.38);background:rgba(45,245,196,.08);color:#2df5c4;border-radius:999px;padding:11px 15px;font-weight:950;display:flex;align-items:center;gap:9px}
.live span{width:10px;height:10px;border-radius:50%;background:#2df5c4;box-shadow:0 0 20px #2df5c4;animation:pulse 1.2s infinite}
.metric-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-top:20px;position:relative;z-index:1}
.metric{border:1px solid rgba(86,166,255,.22);border-radius:22px;padding:16px;background:linear-gradient(145deg,rgba(12,23,38,.92),rgba(8,14,24,.80));box-shadow:0 16px 50px rgba(0,0,0,.30);transition:.18s ease}
.metric:hover{transform:translateY(-3px);border-color:rgba(45,245,196,.52);box-shadow:0 0 38px rgba(45,245,196,.12)}
.metric small{display:block;color:#94a8bb;text-transform:uppercase;letter-spacing:.11em;font-size:10px;font-weight:950}
.metric b{display:block;color:#fff;font-size:26px;line-height:1.2;margin-top:5px}
.metric em{display:block;color:#2df5c4;font-style:normal;font-size:12px;font-weight:800;margin-top:3px}
.panel{border:1px solid rgba(86,166,255,.22);border-radius:25px;padding:16px;background:rgba(9,17,28,.76);box-shadow:0 18px 60px rgba(0,0,0,.30)}
.panel h3{margin:0 0 12px 0!important;color:#f4fbff!important;font-size:19px!important}
.ops-grid{display:grid;grid-template-columns:1.45fr 1fr;gap:14px;margin-top:14px}
.lower-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:14px}
.feed{display:flex;gap:12px;align-items:center;padding:12px;border-radius:16px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.075);margin-bottom:9px}
.feed span{width:10px;height:10px;border-radius:50%;background:#2df5c4;box-shadow:0 0 18px #2df5c4}
.feed.warn span{background:#ffbf4d;box-shadow:0 0 18px #ffbf4d}.feed.crit span{background:#ff3860;box-shadow:0 0 18px #ff3860}
.feed b{color:#fff}.feed small{display:block;color:#9fb3c8;margin-top:2px}
.action-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.action{border:1px solid rgba(45,245,196,.24);background:rgba(45,245,196,.075);color:#eafff9;border-radius:18px;padding:14px;font-weight:950;text-align:center;transition:.18s ease}
.action:hover{transform:scale(1.02);box-shadow:0 0 28px rgba(45,245,196,.13)}
.ai-card{padding:14px;border-radius:18px;border:1px solid rgba(45,245,196,.2);background:rgba(45,245,196,.055);color:#dffcf6;font-weight:800;margin-bottom:10px}
.ai-card b{display:block;color:#fff;margin-bottom:4px}
.footer{margin-top:16px;border:1px solid rgba(45,245,196,.20);background:rgba(45,245,196,.055);border-radius:18px;padding:14px;text-align:center;color:#2df5c4;font-weight:950}
@media(max-width:1150px){.metric-grid{grid-template-columns:1fr 1fr 1fr}.ops-grid,.lower-grid{grid-template-columns:1fr}}
@media(max-width:650px){.metric-grid,.action-grid{grid-template-columns:1fr}.hero-top h1{font-size:38px!important}}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False, ttl=1800)
def quantum_data(seed=77):
    rng = np.random.default_rng(seed)
    hubs = ["Atlantic", "Gulf", "Interior", "Pacific"]
    modes = ["Standard", "Second Class", "First Class", "Same Day"]
    states = ["California","New York","Texas","Florida","Georgia","Arizona","Washington","Ohio","Colorado","Virginia","Kansas","Alabama","Louisiana","Maryland"]
    routes = ["LA-Dallas","NY-Chicago","Miami-Atlanta","Seattle-Denver","Houston-Phoenix","Boston-NYC","Dallas-Orlando","Denver-LA"]
    n = 900
    return pd.DataFrame({
        "Hub": rng.choice(hubs, n), "Mode": rng.choice(modes, n), "State": rng.choice(states, n), "Route": rng.choice(routes, n),
        "AI_Risk": np.clip(rng.normal(42, 20, n), 0, 100),
        "Delay": np.clip(rng.normal(17, 12, n), 0, 100),
        "Cost": rng.normal(520, 125, n),
        "Profit": rng.normal(2200, 560, n),
        "Volume": rng.integers(8, 280, n),
        "ETA": np.clip(rng.normal(3.7, 1.4, n), 1, 10)
    })

df = quantum_data()

st.markdown(f"""
<div class="quantum-hero">
  <div class="hero-top">
    <div>
      <div class="kicker">TITAN ENTERPRISE • PHASE 7 QUANTUM OPS</div>
      <h1>QUANTUM OPS Nexus</h1>
      <p>Enterprise AI logistics control layer with faster cached analytics, tactical decision intelligence, command actions, and stabilized high-performance charts.</p>
    </div>
    <div class="live"><span></span> QUANTUM ONLINE</div>
  </div>
  <div class="metric-grid">
    <div class="metric"><small>Network Volume</small><b>{int(df.Volume.sum()):,}</b><em>shipment flow</em></div>
    <div class="metric"><small>AI Risk</small><b>{df.AI_Risk.mean():.1f}%</b><em>risk index</em></div>
    <div class="metric"><small>Delay Load</small><b>{df.Delay.mean():.1f}%</b><em>SLA pressure</em></div>
    <div class="metric"><small>Profit Signal</small><b>${df.Profit.sum()/1_000_000:.2f}M</b><em>financial pulse</em></div>
    <div class="metric"><small>Avg ETA</small><b>{df.ETA.mean():.1f}d</b><em>delivery forecast</em></div>
    <div class="metric"><small>Routes</small><b>{df.Route.nunique()}</b><em>active lanes</em></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ai-card"><b>🧠 Quantum AI Recommendation</b>
Rebalance capacity from low-risk Interior lanes toward Gulf and Pacific priority routes. Protect Same Day shipments with dedicated SLA monitoring.</div>
""", unsafe_allow_html=True)

st.markdown('<div class="ops-grid">', unsafe_allow_html=True)
c1, c2 = st.columns([1.45, 1])
with c1:
    st.markdown('<div class="panel"><h3>🌌 Quantum Risk Mesh</h3>', unsafe_allow_html=True)
    matrix = df.groupby(["Hub", "Mode"], observed=True).agg(Risk=("AI_Risk","mean")).reset_index()
    pivot = matrix.pivot(index="Hub", columns="Mode", values="Risk").fillna(0)
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=[[0,"#053b75"],[.42,"#2df5c4"],[.70,"#ffbf4d"],[1,"#ff3860"]],
        colorbar=dict(title=dict(text="Risk", font=dict(color="#dcecff")), tickfont=dict(color="#dcecff")),
        hovertemplate="<b>%{y}</b><br>Mode: %{x}<br>Risk: %{z:.1f}%<extra></extra>"
    ))
    fig.update_layout(template="plotly_dark", height=410, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    top = df.groupby("State").agg(Risk=("AI_Risk","mean"), Volume=("Volume","sum"), ETA=("ETA","mean")).sort_values("Risk", ascending=False).head(7)
    items = ""
    for state, row in top.iterrows():
        cls = "crit" if row.Risk > 58 else "warn" if row.Risk > 45 else ""
        items += f'<div class="feed {cls}"><span></span><div><b>{state}</b><small>{row.Risk:.1f}% risk • {int(row.Volume):,} volume • ETA {row.ETA:.1f}d</small></div></div>'
    st.markdown(f'<div class="panel"><h3>⚡ Live Escalation Stream</h3>{items}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

c3, c4, c5 = st.columns(3)
with c3:
    st.markdown('<div class="panel"><h3>📈 Delivery Health Forecast</h3>', unsafe_allow_html=True)
    rng = np.random.default_rng(14)
    x = np.arange(1,25)
    y = 90 + np.cumsum(rng.normal(0, .8, 24))
    fig2 = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color="#2df5c4", width=3), marker=dict(size=6)))
    fig2.update_layout(template="plotly_dark", height=280, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="panel"><h3>🛰 Route Efficiency</h3>', unsafe_allow_html=True)
    route = df.groupby("Route").agg(Eff=("Profit","mean")).sort_values("Eff", ascending=False).head(6)
    fig3 = go.Figure(go.Bar(x=route.Eff, y=route.index, orientation="h", marker=dict(color="#2df5c4")))
    fig3.update_layout(template="plotly_dark", height=280, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
with c5:
    st.markdown("""
    <div class="panel"><h3>🚀 Quantum Actions</h3>
      <div class="action-grid">
        <div class="action">Rebalance Fleet</div><div class="action">Predict Delays</div>
        <div class="action">Optimize Routes</div><div class="action">Generate Report</div>
        <div class="action">SLA Recovery</div><div class="action">Risk Scan</div>
      </div>
    </div>
    <div class="footer">✓ Phase 7 complete • ✓ Faster UX • ✓ More stable charts • ✓ Next-level command UI</div>
    """, unsafe_allow_html=True)
