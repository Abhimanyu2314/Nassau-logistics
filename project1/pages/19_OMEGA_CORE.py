
import streamlit as st
from utils.common import setup_page
import plotly.graph_objects as go
import numpy as np

setup_page("OMEGA CORE")

st.markdown("""
<style>
.stApp{
background:
radial-gradient(circle at 10% 10%,rgba(45,245,196,.12),transparent 28%),
radial-gradient(circle at 90% 12%,rgba(86,166,255,.11),transparent 32%),
radial-gradient(circle at 50% 100%,rgba(178,94,255,.08),transparent 35%),
linear-gradient(135deg,#020611,#050f19 55%,#040912)!important;
}
.block-container{
max-width:1850px!important;
padding-top:1rem!important;
}
.hero{
border:1px solid rgba(45,245,196,.28);
border-radius:38px;
padding:38px;
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
font-size:78px!important;
font-weight:1000!important;
letter-spacing:-.08em;
color:#f3fbff!important;
margin-bottom:8px!important;
position:relative;
z-index:1;
}
.subtitle{
color:#9db0c3!important;
font-size:19px!important;
max-width:1150px;
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
@media(max-width:1000px){
.metric-grid{grid-template-columns:1fr 1fr 1fr}
}
@media(max-width:650px){
.metric-grid{grid-template-columns:1fr 1fr}
.title{font-size:48px!important}
}
</style>
""", unsafe_allow_html=True)

rng = np.random.default_rng(1404)

core_nodes = 256
stability = rng.uniform(90,99.9)
throughput = rng.integers(80000,240000)
risk = rng.uniform(8,58)
efficiency = rng.uniform(94,99.9)

st.markdown(f"""
<div class="hero">
<div class="title">Omega Core</div>
<div class="subtitle">
Ultimate autonomous logistics intelligence core with self-learning orchestration,
adaptive neural routing, quantum-scale optimization,
and executive-grade AI operational supremacy.
</div>

<div class="metric-grid">
<div class="metric"><small>Core Nodes</small><b>{core_nodes}</b><em>autonomous systems</em></div>
<div class="metric"><small>Core Stability</small><b>{stability:.1f}%</b><em>self-healing mesh</em></div>
<div class="metric"><small>Throughput</small><b>{throughput:,}</b><em>live AI processing</em></div>
<div class="metric"><small>Risk Exposure</small><b>{risk:.1f}%</b><em>predictive control</em></div>
<div class="metric"><small>AI Efficiency</small><b>{efficiency:.1f}%</b><em>adaptive optimization</em></div>
<div class="metric"><small>Latency</small><b>4ms</b><em>omega relay speed</em></div>
</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.55,1])

with c1:
    st.markdown('<div class="panel"><h3>🧬 Omega Neural Core</h3>', unsafe_allow_html=True)

    theta = np.linspace(0, 8*np.pi, 500)
    r = np.linspace(0.1, 1.0, 500)

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line=dict(color="#2df5c4", width=3)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=580,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel"><h3>🚨 Omega Autonomous Alerts</h3>', unsafe_allow_html=True)

    sectors = [
        "Neural Freight Cortex",
        "Quantum Fleet Relay",
        "Global Tactical Grid",
        "Autonomous Delivery Nexus",
        "Predictive Supply Core",
        "Executive AI Oversight"
    ]

    for s in sectors:
        val = rng.uniform(5,95)

        if val > 70:
            st.error(f"🚨 **{s}** | Critical neural anomaly detected | Instability **{val:.1f}%**")
        elif val > 40:
            st.warning(f"⚠️ **{s}** | Elevated adaptive variance | Instability **{val:.1f}%**")
        else:
            st.success(f"✅ **{s}** | Stable autonomous operation | Instability **{val:.1f}%**")

    st.info("🧬 Omega Directive: activate autonomous optimization protocols across the global neural mesh.")

    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="panel"><h3>📈 Adaptive Intelligence Stream</h3>', unsafe_allow_html=True)

    x2 = np.linspace(0,50,800)
    y2 = np.sin(x2/2)+np.cos(x2/3)+rng.normal(0,.04,800)

    fig2 = go.Figure(go.Scatter(
        x=x2,
        y=y2,
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
    st.markdown('<div class="panel"><h3>🚀 Omega Autonomous Command</h3>', unsafe_allow_html=True)

    st.success("Activate autonomous logistics orchestration")
    st.warning("Increase neural optimization bandwidth")
    st.error("Deploy emergency predictive stabilization")
    st.info("Generate omega executive intelligence briefing")
    st.success("Enable adaptive AI recovery mesh")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">✓ Phase 14 complete • ✓ Autonomous Omega Core • ✓ Self-learning AI orchestration • ✓ Quantum adaptive logistics intelligence</div>', unsafe_allow_html=True)
