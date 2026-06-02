
import streamlit as st
from utils.common import setup_page
import plotly.graph_objects as go
import numpy as np

setup_page("QUANTUM GRID")

st.markdown("""
<style>
.stApp{
background:
radial-gradient(circle at 10% 10%,rgba(45,245,196,.12),transparent 28%),
radial-gradient(circle at 90% 12%,rgba(86,166,255,.11),transparent 32%),
linear-gradient(135deg,#020611,#050f19 55%,#040912)!important;
}
.block-container{
max-width:1800px!important;
padding-top:1rem!important;
}
.hero{
border:1px solid rgba(45,245,196,.28);
border-radius:36px;
padding:36px;
background:linear-gradient(145deg,rgba(8,18,31,.96),rgba(8,28,40,.74));
box-shadow:0 30px 120px rgba(0,0,0,.55);
margin-bottom:18px;
position:relative;
overflow:hidden;
}
.hero:before{
content:"";
position:absolute;
inset:-10px;
background:linear-gradient(115deg,transparent,rgba(45,245,196,.18),rgba(86,166,255,.08),transparent);
animation:scan 6s linear infinite;
transform:translateX(-100%);
}
@keyframes scan{
100%{transform:translateX(100%)}
}
.title{
font-size:72px!important;
font-weight:1000!important;
letter-spacing:-.08em;
color:#f3fbff!important;
margin-bottom:8px!important;
position:relative;
z-index:1;
}
.subtitle{
color:#9db0c3!important;
font-size:18px!important;
max-width:1100px;
position:relative;
z-index:1;
}
.metric-grid{
display:grid;
grid-template-columns:repeat(6,1fr);
gap:12px;
margin-top:24px;
position:relative;
z-index:1;
}
.metric{
border:1px solid rgba(255,255,255,.08);
background:rgba(255,255,255,.03);
border-radius:22px;
padding:16px;
transition:.18s ease;
}
.metric:hover{
transform:translateY(-4px);
border-color:rgba(45,245,196,.5);
box-shadow:0 0 28px rgba(45,245,196,.12);
}
.metric small{
display:block;
color:#8ea4ba;
font-size:10px;
font-weight:900;
letter-spacing:.12em;
text-transform:uppercase;
}
.metric b{
display:block;
font-size:28px;
color:white;
margin-top:5px;
}
.metric em{
display:block;
font-style:normal;
color:#2df5c4;
font-size:12px;
margin-top:4px;
font-weight:800;
}
.panel{
border:1px solid rgba(86,166,255,.18);
border-radius:26px;
padding:18px;
background:rgba(9,17,28,.82);
box-shadow:0 18px 60px rgba(0,0,0,.3);
}
.panel h3{
margin:0 0 12px 0!important;
color:#f4fbff!important;
}
.footer{
margin-top:16px;
padding:14px;
text-align:center;
border-radius:18px;
background:rgba(45,245,196,.06);
border:1px solid rgba(45,245,196,.2);
color:#2df5c4;
font-weight:900;
}
.command{
padding:12px;
margin-bottom:10px;
border-radius:16px;
background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.08);
}
.command b{
color:white;
}
.command small{
display:block;
color:#9fb3c8;
margin-top:2px;
}
@media(max-width:1000px){
.metric-grid{grid-template-columns:1fr 1fr 1fr}
}
@media(max-width:650px){
.metric-grid{grid-template-columns:1fr 1fr}
.title{font-size:44px!important}
}
</style>
""", unsafe_allow_html=True)

rng = np.random.default_rng(999)

nodes = 128
stability = rng.uniform(82,99)
risk = rng.uniform(15,92)
efficiency = rng.uniform(85,99)
traffic = rng.integers(12000,78000)

st.markdown(f"""
<div class="hero">
<div class="title">Quantum Grid</div>
<div class="subtitle">
Quantum-scale operational intelligence matrix with holographic node architecture,
predictive logistics mesh analysis, neural command synchronization,
and enterprise AI route orchestration.
</div>

<div class="metric-grid">
<div class="metric"><small>Quantum Nodes</small><b>{nodes}</b><em>active grid systems</em></div>
<div class="metric"><small>Grid Stability</small><b>{stability:.1f}%</b><em>neural synchronization</em></div>
<div class="metric"><small>Risk Exposure</small><b>{risk:.1f}%</b><em>predictive analytics</em></div>
<div class="metric"><small>AI Efficiency</small><b>{efficiency:.1f}%</b><em>optimized routing</em></div>
<div class="metric"><small>Traffic Load</small><b>{traffic:,}</b><em>live operational mesh</em></div>
<div class="metric"><small>Latency</small><b>8ms</b><em>quantum relay speed</em></div>
</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.5,1])

with c1:
    st.markdown('<div class="panel"><h3>⚛️ Quantum Node Matrix</h3>', unsafe_allow_html=True)

    theta = np.linspace(0, 2*np.pi, nodes)
    radius = rng.uniform(0.2,1.0,nodes)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=radius,
        theta=np.degrees(theta),
        mode="markers",
        marker=dict(
            size=10,
            color=radius,
            colorscale="Turbo",
            opacity=0.85
        )
    ))

    fig.update_layout(
        template="plotly_dark",
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10,r=10,t=10,b=10)
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel"><h3>🚨 Quantum Grid Alerts</h3>', unsafe_allow_html=True)

    sectors = [
        "North Grid Cluster",
        "Pacific Relay Mesh",
        "European Quantum Link",
        "Asia Neural Corridor",
        "South Tactical Grid",
        "Middle-East Sync Core"
    ]

    for s in sectors:
        val = rng.uniform(20,95)

        if val > 75:
            st.error(f"🚨 **{s}** | Critical quantum instability detected | Exposure **{val:.1f}%**")
        elif val > 50:
            st.warning(f"⚠️ **{s}** | Elevated operational variance | Exposure **{val:.1f}%**")
        else:
            st.success(f"✅ **{s}** | Stable synchronized state | Exposure **{val:.1f}%**")

    st.info("⚛️ Quantum Directive: reinforce synchronization bandwidth for unstable neural corridors.")

    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="panel"><h3>📡 Quantum Traffic Waveform</h3>', unsafe_allow_html=True)

    x = np.linspace(0,20,400)
    y = np.sin(x)*np.cos(x/2) + rng.normal(0,.05,400)

    fig2 = go.Figure(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line=dict(color="#2df5c4", width=3)
    ))

    fig2.update_layout(
        template="plotly_dark",
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10,r=10,t=10,b=10)
    )

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="panel"><h3>🚀 Quantum Command Layer</h3>', unsafe_allow_html=True)

    st.success("Optimize neural relay channels")
    st.warning("Increase quantum route stabilization")
    st.error("Deploy emergency synchronization protocols")
    st.info("Generate enterprise quantum intelligence briefing")
    st.success("Activate autonomous AI orchestration")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">✓ Phase 13 complete • ✓ Quantum logistics mesh • ✓ Holographic node intelligence • ✓ Autonomous AI orchestration</div>', unsafe_allow_html=True)
