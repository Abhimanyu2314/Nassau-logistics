
import streamlit as st
from utils.common import setup_page
import plotly.graph_objects as go
import numpy as np
import pandas as pd

setup_page("GLOBAL COMMAND CENTER")

st.markdown("""
<style>
.stApp{
background:
radial-gradient(circle at 10% 10%,rgba(45,245,196,.12),transparent 28%),
radial-gradient(circle at 90% 12%,rgba(86,166,255,.10),transparent 32%),
linear-gradient(135deg,#030711,#06101b 55%,#040912)!important;
}
.block-container{max-width:1700px!important;padding-top:1rem!important}
.hero{
border:1px solid rgba(45,245,196,.28);
border-radius:34px;
padding:32px;
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
@keyframes scan{100%{transform:translateX(100%)}}
.title{
font-size:64px!important;
font-weight:1000!important;
letter-spacing:-.07em;
color:#f3fbff!important;
margin-bottom:8px!important;
position:relative;
z-index:1;
}
.subtitle{
color:#9db0c3!important;
font-size:18px!important;
max-width:980px;
position:relative;
z-index:1;
}
.metric-grid{
display:grid;
grid-template-columns:repeat(6,1fr);
gap:12px;
margin-top:22px;
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
@media(max-width:1000px){
.metric-grid{grid-template-columns:1fr 1fr 1fr}
}
@media(max-width:650px){
.metric-grid{grid-template-columns:1fr 1fr}
.title{font-size:40px!important}
}
</style>
""", unsafe_allow_html=True)

rng = np.random.default_rng(404)

regions = ["North America","Europe","Asia Pacific","South America","Middle East","Africa"]
risk = rng.uniform(20,95, len(regions))
volume = rng.integers(1000,9000,len(regions))
sla = rng.uniform(82,99,len(regions))

st.markdown(f"""
<div class="hero">
<div class="title">Global Command Center</div>
<div class="subtitle">
Worldwide operational intelligence layer with predictive monitoring,
global route risk tracking, executive command analytics, and AI-driven tactical oversight.
</div>

<div class="metric-grid">
<div class="metric"><small>Global Shipments</small><b>{volume.sum():,}</b><em>live worldwide volume</em></div>
<div class="metric"><small>Avg Risk</small><b>{risk.mean():.1f}%</b><em>global AI signal</em></div>
<div class="metric"><small>SLA Health</small><b>{sla.mean():.1f}%</b><em>delivery efficiency</em></div>
<div class="metric"><small>Critical Zones</small><b>{(risk>70).sum()}</b><em>active escalations</em></div>
<div class="metric"><small>Operational Nodes</small><b>148</b><em>connected centers</em></div>
<div class="metric"><small>Fleet Capacity</small><b>92.7%</b><em>global readiness</em></div>
</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.45,1])

with c1:
    st.markdown('<div class="panel"><h3>🌐 Global Risk Radar</h3>', unsafe_allow_html=True)

    fig = go.Figure(go.Scatterpolar(
        r=risk,
        theta=regions,
        fill='toself',
        line=dict(color="#2df5c4", width=3),
        marker=dict(size=9, color=risk, colorscale="Turbo")
    ))

    fig.update_layout(
        template="plotly_dark",
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20,r=20,t=20,b=20)
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel"><h3>🚨 Executive Escalation Matrix</h3>', unsafe_allow_html=True)

    for reg, r, v, s in zip(regions, risk, volume, sla):
        if r > 75:
            st.error(f"🚨 **{reg}** | Risk **{r:.1f}%** | Volume **{v:,}** | SLA **{s:.1f}%**")
        elif r > 50:
            st.warning(f"⚠️ **{reg}** | Risk **{r:.1f}%** | Volume **{v:,}** | SLA **{s:.1f}%**")
        else:
            st.success(f"✅ **{reg}** | Risk **{r:.1f}%** | Volume **{v:,}** | SLA **{s:.1f}%**")

    st.info("🧠 AI Directive: shift premium fleet allocation toward high-risk global corridors.")
    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="panel"><h3>📈 Predictive Operations Timeline</h3>', unsafe_allow_html=True)

    x = list(range(1,31))
    y = 70 + np.cumsum(rng.normal(0,1.5,30))

    fig2 = go.Figure(go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        line=dict(color="#2df5c4", width=3),
        marker=dict(size=6)
    ))

    fig2.update_layout(
        template="plotly_dark",
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10,r=10,t=10,b=10)
    )

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="panel"><h3>🛰 Tactical AI Directives</h3>', unsafe_allow_html=True)

    st.success("Optimize Asia-Pacific high-volume routes")
    st.warning("Monitor North America delay escalation")
    st.error("Deploy emergency fleet to Europe corridor")
    st.info("Generate global executive intelligence report")
    st.success("Activate predictive SLA recovery mode")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">✓ Phase 11 complete • ✓ Global command intelligence • ✓ Executive tactical analytics • ✓ Worldwide monitoring system</div>', unsafe_allow_html=True)
