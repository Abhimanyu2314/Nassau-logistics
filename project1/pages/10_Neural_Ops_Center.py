import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.common import setup_page, brand_header, load_data
from backend.api.enterprise_service import build_enterprise_context
from backend.ai_engine.neural_ops import NeuralOpsEngine

setup_page("Neural Ops Center")
brand_header()

st.markdown("""
<style>
.neural-hero{position:relative;overflow:hidden;background:radial-gradient(circle at 20% 20%,rgba(41,211,145,.32),transparent 28%),radial-gradient(circle at 90% 0%,rgba(85,166,255,.26),transparent 30%),linear-gradient(135deg,#09111d,#121b2c 55%,#07110f);border:1px solid rgba(41,211,145,.35);border-radius:32px;padding:32px;margin-bottom:20px;box-shadow:0 0 70px rgba(41,211,145,.12)}
.neural-hero:after{content:"";position:absolute;inset:-40%;background:linear-gradient(120deg,transparent,rgba(255,255,255,.09),transparent);animation:sweep 5s linear infinite}.neural-hero>*{position:relative;z-index:1}@keyframes sweep{from{transform:translateX(-35%) rotate(12deg)}to{transform:translateX(35%) rotate(12deg)}}
.neural-title{font-size:2.6rem;font-weight:950;letter-spacing:-.05em;color:white}.neural-sub{color:#b8c7d9;font-size:1.05rem}.omega-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;margin:16px 0}.omega-card{background:linear-gradient(145deg,rgba(22,31,45,.88),rgba(10,16,25,.88));border:1px solid rgba(85,166,255,.22);border-radius:24px;padding:18px;box-shadow:0 16px 50px rgba(0,0,0,.28);transition:.28s ease}.omega-card:hover{transform:translateY(-5px) scale(1.01);box-shadow:0 0 36px rgba(41,211,145,.18);border-color:rgba(41,211,145,.48)}.omega-label{font-size:.72rem;color:#aab6c4;text-transform:uppercase;letter-spacing:.14em}.omega-value{font-size:1.9rem;color:#fff;font-weight:950;margin-top:5px}.briefing{background:rgba(9,17,29,.78);border:1px solid rgba(41,211,145,.28);border-radius:22px;padding:18px;box-shadow:0 0 30px rgba(41,211,145,.08)}.briefing li{margin:.45rem 0;color:#dff7ee}.status-dot{display:inline-block;width:9px;height:9px;border-radius:999px;background:#29d391;box-shadow:0 0 20px #29d391;margin-right:7px}@media(max-width:1000px){.omega-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.neural-title{font-size:1.8rem}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="neural-hero">
  <div class="neural-title">⚡ TITAN PHASE 4 — NEURAL OPS CENTER</div>
  <div class="neural-sub">Predictive control tower • fleet watch radar • regional command intelligence • executive AI briefing</div>
</div>
""", unsafe_allow_html=True)

if st.button("⬅ Back to Main Dashboard"):
    st.switch_page("app.py")

df = load_data()
ctx = build_enterprise_context(df)
scored = ctx["scored_shipments"]
neural = NeuralOpsEngine(scored)
summary = neural.control_tower_summary()
timeline = neural.mission_timeline()
radar = neural.regional_radar()
watch = neural.fleet_watch(35)

st.markdown(f"""
<div class="omega-grid">
  <div class="omega-card"><div class="omega-label">Active Shipments</div><div class="omega-value">{summary['active_shipments']:,}</div></div>
  <div class="omega-card"><div class="omega-label">Critical Shipments</div><div class="omega-value">{summary['critical_shipments']:,}</div></div>
  <div class="omega-card"><div class="omega-label">Critical %</div><div class="omega-value">{summary['critical_percent']}%</div></div>
  <div class="omega-card"><div class="omega-label">Network Health</div><div class="omega-value">{summary['network_health']}%</div></div>
  <div class="omega-card"><div class="omega-label">Profit Protected</div><div class="omega-value">${summary['profit_protected']:,.0f}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🧠 Executive AI Briefing")
items = "".join([f"<li><span class='status-dot'></span>{x}</li>" for x in neural.ai_briefing()])
st.markdown(f"<div class='briefing'><ul>{items}</ul></div>", unsafe_allow_html=True)

st.markdown("### 🎛 Neural command filters")
c1, c2, c3 = st.columns(3)
with c1:
    region = st.selectbox("Region", ["All"] + sorted(scored["Region"].dropna().unique().tolist()))
with c2:
    mode = st.selectbox("Ship Mode", ["All"] + sorted(scored["Ship Mode"].dropna().unique().tolist()))
with c3:
    status = st.selectbox("Ops Status", ["All", "RED ALERT", "ACTIVE WATCH", "NORMAL"])

view = watch.copy()
if region != "All": view = view[view["Region"] == region]
if mode != "All": view = view[view["Ship Mode"] == mode]
if status != "All": view = view[view["Ops_Status"] == status]

left, right = st.columns([1.15, .85])
with left:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeline["Period"], y=timeline["Shipments"], mode="lines+markers", name="Shipments"))
    fig.add_trace(go.Scatter(x=timeline["Period"], y=timeline["Neural_Load"], mode="lines+markers", name="Neural Load"))
    fig.update_layout(template="plotly_dark", height=430, title="Cinematic mission timeline", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.bar(radar, x="Avg_Risk", y="Region", color="Command_Status", orientation="h", title="Regional command radar")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🚨 Live Fleet Watch Radar")
st.dataframe(view, use_container_width=True, height=420)
st.download_button("⬇ Export Neural Ops Watchlist", view.to_csv(index=False), "phase4_neural_ops_watchlist.csv", "text/csv")

st.markdown("### 🌐 Profit-risk command matrix")
fig = px.scatter(scored, x="Gross Profit", y="AI Risk Score", color="Region", size="Lead Time", hover_data=["Order ID", "State/Province", "Ship Mode"], title="Shipment profit exposure vs AI risk")
fig.update_layout(template="plotly_dark", height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)
