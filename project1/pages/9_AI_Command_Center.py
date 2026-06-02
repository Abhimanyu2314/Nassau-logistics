
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.common import setup_page, brand_header, load_data
from backend.api.enterprise_service import build_enterprise_context

setup_page("AI Command Center")
brand_header()

st.markdown("""
<style>
.command-hero{background:radial-gradient(circle at top left,rgba(41,211,145,.25),transparent 35%),linear-gradient(135deg,#111923,#172234);border:1px solid #2f3a48;border-radius:28px;padding:28px;margin-bottom:18px;box-shadow:0 22px 70px rgba(0,0,0,.35)}
.command-title{font-size:2.35rem;font-weight:950;letter-spacing:-.04em;color:#fff}.command-sub{color:#aab6c4;font-size:1.05rem;margin-top:8px}.matrix-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:18px 0}.matrix-card{background:linear-gradient(145deg,rgba(29,37,48,.92),rgba(15,23,34,.92));border:1px solid rgba(85,166,255,.25);border-radius:22px;padding:18px;box-shadow:0 16px 48px rgba(0,0,0,.25);transition:.25s ease}.matrix-card:hover{transform:translateY(-4px);box-shadow:0 0 35px rgba(41,211,145,.16)}.matrix-label{font-size:.8rem;color:#aab6c4;text-transform:uppercase;letter-spacing:.12em}.matrix-value{font-size:2rem;color:#fff;font-weight:900}.copilot{background:#101820;border:1px solid rgba(41,211,145,.35);border-radius:22px;padding:18px;box-shadow:0 0 35px rgba(41,211,145,.08)}.pulse{display:inline-block;width:10px;height:10px;border-radius:50%;background:#29d391;box-shadow:0 0 20px #29d391;margin-right:8px}.stButton>button{border-radius:14px!important;font-weight:800!important}
@media(max-width:900px){.matrix-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.command-title{font-size:1.7rem}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="command-hero">
  <div class="command-title">🧠 TITAN PHASE 2 — AI COMMAND CENTER</div>
  <div class="command-sub">Route optimizer • AI copilot prompts • tactical lane scorecards • predictive risk radar • database activity stream</div>
</div>
""", unsafe_allow_html=True)

if st.button("⬅ Back to Main Dashboard"):
    st.switch_page("app.py")

df = load_data()
ctx = build_enterprise_context(df)
scored = ctx["scored_shipments"]
summary = ctx["summary"]
lanes = ctx["lane_scorecard"]
actions = ctx["next_actions"]

st.markdown(f"""
<div class="matrix-grid">
  <div class="matrix-card"><div class="matrix-label">AI Avg Risk</div><div class="matrix-value">{summary['avg_risk']}%</div></div>
  <div class="matrix-card"><div class="matrix-label">High Risk</div><div class="matrix-value">{summary['high_risk']:,}</div></div>
  <div class="matrix-card"><div class="matrix-label">Critical Lanes</div><div class="matrix-value">{int((lanes['Priority'].astype(str)=='Critical').sum()):,}</div></div>
  <div class="matrix-card"><div class="matrix-label">Delay Rate</div><div class="matrix-value">{summary['delay_rate']}%</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🎛 Tactical command filters")
c1,c2,c3 = st.columns(3)
with c1:
    region = st.selectbox("Region", ["All"] + sorted(scored["Region"].dropna().unique().tolist()))
with c2:
    mode = st.selectbox("Ship Mode", ["All"] + sorted(scored["Ship Mode"].dropna().unique().tolist()))
with c3:
    priority = st.selectbox("Lane Priority", ["All", "Critical", "Watch", "Optimized"])

lane_view = lanes.copy()
if region != "All": lane_view = lane_view[lane_view["Region"] == region]
if mode != "All": lane_view = lane_view[lane_view["Ship Mode"] == mode]
if priority != "All": lane_view = lane_view[lane_view["Priority"].astype(str) == priority]

st.markdown("### 🛰 Route Optimization Matrix")
left, right = st.columns([1.15, .85])
with left:
    fig = px.scatter(lane_view, x="Shipments", y="Optimization_Score", size="Avg_Risk", color="Priority", hover_data=["Region","State/Province","Ship Mode","Delay_Rate"], title="Lane optimization radar")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with right:
    top_states = scored.groupby("State/Province", observed=True).agg(Avg_Risk=("AI Risk Score","mean"), Shipments=("Order ID","count"), Delay=("Delayed","mean")).reset_index().sort_values("Avg_Risk", ascending=False).head(12)
    top_states["Delay"] = top_states["Delay"]*100
    fig = px.bar(top_states, x="Avg_Risk", y="State/Province", orientation="h", title="Highest AI-risk markets")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🤖 AI Copilot Command Console")
question = st.text_input("Ask logistics copilot", placeholder="Example: show critical lanes in Atlantic region")
if question:
    q = question.lower()
    response = "I recommend opening the critical lane scorecard and prioritizing high delay + high shipment lanes."
    if "critical" in q:
        response = f"There are {int((lanes['Priority'].astype(str)=='Critical').sum())} critical lanes. Focus on lanes with lowest optimization score first."
    elif "profit" in q:
        response = f"Current gross profit is ${summary['profit']:,.0f}. Protect high-profit lanes with elevated delay risk."
    elif "delay" in q:
        response = f"Current delay rate is {summary['delay_rate']}%. Escalate high-risk states and review Same Day/First Class SLA pressure."
    elif "route" in q or "lane" in q:
        worst = lanes.sort_values("Optimization_Score").head(1).iloc[0]
        response = f"Weakest lane: {worst['Region']} → {worst['State/Province']} using {worst['Ship Mode']} with optimization score {worst['Optimization_Score']}."
    st.markdown(f"<div class='copilot'><span class='pulse'></span><b>AI Copilot:</b> {response}</div>", unsafe_allow_html=True)

st.markdown("### ✅ Recommended next actions")
st.dataframe(actions, use_container_width=True, height=260)

st.markdown("### 📋 Tactical lane scorecard")
st.dataframe(lane_view.sort_values("Optimization_Score").head(75), use_container_width=True, height=430)
st.download_button("⬇ Export Phase 2 Lane Scorecard", lane_view.to_csv(index=False), "phase2_lane_scorecard.csv", "text/csv")

st.markdown("### 🧾 Database activity stream")
st.dataframe(ctx["activity"], use_container_width=True)
