import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.common import setup_page, brand_header, page_loader, hero, load_data, route_metrics, state_metrics, command_center, smart_insight_cards, enhanced_v4_panel, v4_priority_lanes, v4_action_dock, v5_hyper_css, v5_hyper_command_center, v5_route_intelligence_panel, v5_floating_dock, holographic_command_center, floating_action_command_menu, elite_heatmap_section, executive_operations_overview

setup_page("Nassau Logistics AI")
v5_hyper_css()
page_loader("Opening Logistics Intelligence Center")
brand_header()

hero(
    "Factory-to-Customer Shipping Intelligence",
    "Advanced logistics analytics platform for route efficiency, geographic bottlenecks, ship-mode intelligence, and AI-powered shipment prediction."
)

df = load_data()
routes = route_metrics(df)
v5_hyper_command_center(df, routes)
holographic_command_center(df, routes)
floating_action_command_menu()
command_center(df, routes)
smart_insight_cards(df, routes)
enhanced_v4_panel(df, routes)
v4_priority_lanes(routes)
st.markdown("<a id='advanced-route-intelligence-widgets'></a>", unsafe_allow_html=True)
v5_route_intelligence_panel(df, routes)
executive_operations_overview(df, routes)
elite_heatmap_section(df)
v4_action_dock()
v5_floating_dock()
states = state_metrics(df)
shipments = len(df)
avg_lead = df["Lead Time"].mean()
delay_rate = df["Delayed"].mean() * 100
profit_k = df["Gross Profit"].sum() / 1000
best_route = routes.iloc[0]["Route"] if len(routes) else "No route"
worst_state = states.sort_values(["Delay_Rate", "Avg_Lead_Time"], ascending=False).iloc[0]["State/Province"] if len(states) else "No state"

st.markdown(f"""
<div class='premium-metric-grid'>
    <div class='premium-mini-card'>
        <div class='premium-mini-icon'>📦</div>
        <div class='premium-mini-label'>Shipments</div>
        <div class='premium-mini-value'>{shipments:,}</div>
        <div class='premium-mini-sub'>live dataset loaded</div>
    </div>
    <div class='premium-mini-card'>
        <div class='premium-mini-icon'>⏱️</div>
        <div class='premium-mini-label'>Avg Lead Time</div>
        <div class='premium-mini-value'>{avg_lead:.1f} d</div>
        <div class='premium-mini-sub'>order to ship cycle</div>
    </div>
    <div class='premium-mini-card'>
        <div class='premium-mini-icon'>⚡</div>
        <div class='premium-mini-label'>Delay Risk</div>
        <div class='premium-mini-value'>{delay_rate:.1f}%</div>
        <div class='premium-mini-sub'>SLA intelligence active</div>
    </div>
    <div class='premium-mini-card'>
        <div class='premium-mini-icon'>💰</div>
        <div class='premium-mini-label'>Gross Profit</div>
        <div class='premium-mini-value'>${profit_k:,.1f}K</div>
        <div class='premium-mini-sub'>executive financial view</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.4, 1])
with col1:
    st.markdown(f"""
    <div class='route-card'>
        <div class='route-title'>Best live route</div>
        <div class='route-value'>{best_route.replace('→', '<br><span class="route-arrow">→</span>')}</div>
        <div class='route-score'>Optimized • Animated • Executive Ready</div>
        <div class='ai-live-indicator'><span></span> AI route intelligence running</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Platform Status</div>
        <div class='metric-value'>LIVE</div>
        <div class='metric-sub'>Critical bottleneck watch: {worst_state}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<a id='quick-command-actions'></a>", unsafe_allow_html=True)
st.markdown("### Quick command actions")
q1, q2, q3, q4 = st.columns(4)
with q1:
    if st.button("⚡ Route Command", use_container_width=True):
        st.switch_page("pages/2_Route_Efficiency.py")
with q2:
    if st.button("🗺️ Geo Map", use_container_width=True):
        st.switch_page("pages/3_Geographic_Analysis.py")
with q3:
    if st.button("🤖 AI Predictor", use_container_width=True):
        st.switch_page("pages/6_AI_Prediction.py")
with q4:
    if st.button("📊 Executive View", use_container_width=True):
        st.switch_page("pages/7_Executive_Summary.py")



st.markdown("### 🚀 Enterprise AI Platform")
st.info("Titan foundation added: AI risk scoring, SQLite enterprise database layer, predictive cockpit, high-risk shipment watchlist, and exportable AI operations data.")
if st.button("🚀 Open Enterprise AI Platform", use_container_width=True):
    st.switch_page("pages/8_Enterprise_AI_Platform.py")



st.markdown("### 🧠 Phase 2 AI Command Center")
st.info("Phase 2 added: tactical lane optimizer, AI copilot console, predictive route scorecards, database activity stream, and exportable operations intelligence.")
if st.button("🧠 Open AI Command Center", use_container_width=True):
    st.switch_page("pages/9_AI_Command_Center.py")



st.markdown("### ⚡ Phase 4 Neural Ops Center")
st.success("Phase 4 added: predictive control tower, regional command radar, fleet watch alerts, mission timeline, and executive AI briefing.")
if st.button("⚡ Open Neural Ops Center", use_container_width=True):
    st.switch_page("pages/10_Neural_Ops_Center.py")

st.markdown("### Working dashboard options")
st.markdown("""
<div class='module-grid'>
    <div class='module-card'><div class='module-icon'>🚚</div><div class='module-title'>Route Efficiency</div><div class='module-copy'>Top/bottom routes, efficiency score, delay frequency, profit, and downloadable results.</div></div>
    <div class='module-card'><div class='module-icon'>🗺️</div><div class='module-title'>Geographic Analysis</div><div class='module-copy'>State heatmap, factory-to-state route network, and bottleneck table.</div></div>
    <div class='module-card'><div class='module-icon'>📦</div><div class='module-title'>Ship Mode Analysis</div><div class='module-copy'>Compare Same Day, First Class, Second Class, and Standard Class performance.</div></div>
    <div class='module-card'><div class='module-icon'>✅</div><div class='module-title'>Data Quality</div><div class='module-copy'>Validation checks, missing values, lead-time rules, and cleaned data preview.</div></div>
    <div class='module-card'><div class='module-icon'>🤖</div><div class='module-title'>AI Prediction</div><div class='module-copy'>Train a delay model and test future shipment scenarios.</div></div>
    <div class='module-card'><div class='module-icon'>📊</div><div class='module-title'>Executive Summary</div><div class='module-copy'>Stakeholder-ready conclusion, risks, and recommendations.</div></div>
</div>
""", unsafe_allow_html=True)

b1,b2,b3 = st.columns(3)
with b1:
    if st.button("🚚 Open Route Efficiency", use_container_width=True):
        st.switch_page("pages/2_Route_Efficiency.py")
    if st.button("✅ Open Data Quality", use_container_width=True):
        st.switch_page("pages/5_Data_Quality.py")
with b2:
    if st.button("🗺️ Open Geographic Analysis", use_container_width=True):
        st.switch_page("pages/3_Geographic_Analysis.py")
    if st.button("🤖 Open AI Prediction", use_container_width=True):
        st.switch_page("pages/6_AI_Prediction.py")
with b3:
    if st.button("📦 Open Ship Mode Analysis", use_container_width=True):
        st.switch_page("pages/4_Ship_Mode_Analysis.py")
    if st.button("📊 Open Executive Summary", use_container_width=True):
        st.switch_page("pages/7_Executive_Summary.py")

st.markdown("### Animated executive charts")
c1, c2 = st.columns(2)
with c1:
    monthly = df.groupby("Month", observed=True).agg(Shipments=("Order ID", "count"), Profit=("Gross Profit", "sum")).reset_index()
    fig = px.line(monthly, x="Month", y="Shipments", markers=True, title="Monthly shipment flow")
    fig.update_traces(line_shape="spline")
    fig.update_layout(template="plotly_dark", height=390, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    top = routes.head(10).sort_values("Efficiency_Score")
    fig = px.bar(top, x="Efficiency_Score", y="Route", orientation="h", title="Top route efficiency leaderboard", color="Efficiency_Score", color_continuous_scale="Teal")
    fig.update_layout(template="plotly_dark", height=390, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)



st.markdown("### Live route network visualization")
map_routes = routes.dropna(subset=["Factory_Lat", "Factory_Lon", "State_Lat", "State_Lon"]).head(35)
fig = go.Figure()
for _, r in map_routes.iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[r["Factory_Lon"], r["State_Lon"]],
        lat=[r["Factory_Lat"], r["State_Lat"]],
        mode="lines",
        line=dict(width=max(1, min(6, r["Shipments"] / 25)), color="rgba(41,211,145,0.45)"),
        hoverinfo="text",
        text=f"{r['Route']}<br>Shipments: {int(r['Shipments'])}<br>Efficiency: {r['Efficiency_Score']:.1f}"
    ))
fig.add_trace(go.Scattergeo(
    lon=list(map_routes["Factory_Lon"]) + list(map_routes["State_Lon"]),
    lat=list(map_routes["Factory_Lat"]) + list(map_routes["State_Lat"]),
    mode="markers",
    marker=dict(size=8, color="rgba(85,166,255,0.95)", line=dict(width=1, color="white")),
    hoverinfo="skip"
))
fig.update_geos(scope="north america", projection_type="albers usa", showland=True, landcolor="rgb(16,24,36)", showlakes=True, lakecolor="rgb(10,15,23)", bgcolor="rgba(0,0,0,0)")
fig.update_layout(template="plotly_dark", height=520, margin=dict(l=0, r=0, t=40, b=0), title="Factory-to-customer route network", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### AI operations console")
st.markdown(f"""
<div class="ai-console">
  <div class="console-top"><span class="console-dot"></span> AI route optimizer online</div>
  <div class="typing-line">Analyzing {shipments:,} shipments • Best route: {best_route} • Bottleneck watch: {worst_state}</div>
  <div class="console-grid">
    <div><b>{routes['Route'].nunique():,}</b><span> Active routes</span></div>
    <div><b>{df['State/Province'].nunique():,}</b><span> Markets covered</span></div>
    <div><b>{df['Ship Mode'].nunique():,}</b><span> Ship modes</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='floating-dock'>
    <div class='dock-pill'>Animated sidebar</div>
    <div class='dock-pill'>Live KPIs</div>
    <div class='dock-pill'>Route map</div>
    <div class='dock-pill'>AI loading</div>
    <div class='dock-pill'>Microinteractions</div>
</div>
""", unsafe_allow_html=True)
