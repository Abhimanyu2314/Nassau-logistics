from utils.fixed_feed import render_ai_escalation_feed

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.common import setup_page, brand_header, load_data
from backend.api.enterprise_service import build_enterprise_context


def render_native_ai_escalation_feed(feed_df):
    st.markdown("### ⚡ AI Escalation Feed")
    st.caption("Real-time high-risk logistics alerts prioritized by AI")

    top_feed = feed_df.sort_values("Avg_AI_Risk", ascending=False).head(5).copy()

    for idx, r in top_feed.iterrows():
        state_name = str(r.get("State/Province", "Unknown"))
        risk_zone = str(r.get("Risk Zone", "Critical"))
        risk_score = float(r.get("Avg_AI_Risk", 0))
        shipments = int(r.get("Shipments", 0))

        if risk_zone.lower() == "critical":
            st.error(f"🚨 **{state_name}**  |  {risk_zone}  |  Risk: **{risk_score:.1f}%**  |  Shipments: **{shipments:,}**")
        elif risk_zone.lower() == "high":
            st.warning(f"⚠️ **{state_name}**  |  {risk_zone}  |  Risk: **{risk_score:.1f}%**  |  Shipments: **{shipments:,}**")
        else:
            st.info(f"🔎 **{state_name}**  |  {risk_zone}  |  Risk: **{risk_score:.1f}%**  |  Shipments: **{shipments:,}**")

    st.success("🤖 Recommendation: rebalance capacity toward the top two risk states and protect fast ship modes for SLA recovery.")



setup_page("Enterprise AI Platform")
brand_header()

with open("frontend/themes/enterprise.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="enterprise-shell">
  <h1 class="enterprise-title">🚀 TITAN ENTERPRISE AI LOGISTICS PLATFORM</h1>
  <div class="enterprise-sub">Real AI-style risk scoring • SQLite enterprise data layer • predictive operations cockpit • executive command intelligence</div>
  <div style="margin-top:14px">
    <span class="ai-pill"><span class="pulse-dot"></span> AI engine online</span>
    <span class="ai-pill"><span class="pulse-dot"></span> Database synced</span>
    <span class="ai-pill"><span class="pulse-dot"></span> Predictive cockpit active</span>
  </div>
</div>
""", unsafe_allow_html=True)

if st.button("⬅ Back to Main Dashboard", use_container_width=False):
    st.switch_page("app.py")

df = load_data()
ctx = build_enterprise_context(df)
scored = ctx["scored_shipments"]
s = ctx["summary"]

st.markdown(f"""
<div class="elite-grid">
  <div class="elite-card"><div class="elite-label">Total Shipments</div><div class="elite-value">{s['shipments']:,}</div></div>
  <div class="elite-card"><div class="elite-label">High Risk Shipments</div><div class="elite-value">{s['high_risk']:,}</div></div>
  <div class="elite-card"><div class="elite-label">Average AI Risk</div><div class="elite-value">{s['avg_risk']}%</div></div>
  <div class="elite-card"><div class="elite-label">Delay Rate</div><div class="elite-value">{s['delay_rate']}%</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🎛 Enterprise Filters")
c1,c2,c3 = st.columns(3)
with c1:
    region = st.selectbox("Region", ["All"] + sorted(scored["Region"].dropna().unique().tolist()))
with c2:
    mode = st.selectbox("Ship mode", ["All"] + sorted(scored["Ship Mode"].dropna().unique().tolist()))
with c3:
    risk = st.selectbox("AI risk level", ["All", "High", "Medium", "Low"])

view = scored.copy()
if region != "All": view = view[view["Region"] == region]
if mode != "All": view = view[view["Ship Mode"] == mode]
if risk != "All": view = view[view["AI Risk Level"].astype(str) == risk]

st.markdown("### 🧠 Neural Risk Intelligence")
col1, col2 = st.columns([1.1,1])
with col1:
    fig = px.histogram(view, x="AI Risk Score", color="AI Risk Level", nbins=30, title="AI shipment risk distribution")
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    risk_by_mode = view.groupby("Ship Mode", observed=True).agg(Avg_Risk=("AI Risk Score","mean"), Shipments=("Order ID","count")).reset_index()
    fig = px.scatter(risk_by_mode, x="Shipments", y="Avg_Risk", size="Shipments", color="Ship Mode", title="Mode risk command radar")
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🛰 AI Tactical Logistics Intelligence Map")

state_risk = view.groupby("State/Province", observed=True).agg(
    Avg_AI_Risk=("AI Risk Score","mean"),
    Shipments=("Order ID","count"),
    Delay_Rate=("Delayed","mean"),
    Avg_Lead_Time=("Lead Time","mean"),
    Profit=("Gross Profit","sum")
).reset_index()

state_risk["Delay_Rate"] = (state_risk["Delay_Rate"] * 100).round(1)
state_risk["Avg_AI_Risk"] = state_risk["Avg_AI_Risk"].round(1)
state_risk["Avg_Lead_Time"] = state_risk["Avg_Lead_Time"].round(1)
state_risk["Profit"] = state_risk["Profit"].round(0)

# State coordinate intelligence layer
STATE_COORDS = {
    "Alabama": (32.806671,-86.791130), "Arizona": (33.729759,-111.431221),
    "Arkansas": (34.969704,-92.373123), "California": (36.116203,-119.681564),
    "Colorado": (39.059811,-105.311104), "Connecticut": (41.597782,-72.755371),
    "Florida": (27.766279,-81.686783), "Georgia": (33.040619,-83.643074),
    "Kansas": (38.526600,-96.726486), "Louisiana": (31.169546,-91.867805),
    "Maryland": (39.063946,-76.802101), "Missouri": (38.456085,-92.288368),
    "Nebraska": (41.125370,-98.268082), "New Hampshire": (43.452492,-71.563896),
    "New York": (42.165726,-74.948051), "Ohio": (40.388783,-82.764915),
    "Rhode Island": (41.680893,-71.511780), "South Carolina": (33.856892,-80.945007),
    "Virginia": (37.769337,-78.169968), "Washington": (47.400902,-121.490494),
    "West Virginia": (38.491226,-80.954453)
}

state_risk["Lat"] = state_risk["State/Province"].map(lambda x: STATE_COORDS.get(x, (None, None))[0])
state_risk["Lon"] = state_risk["State/Province"].map(lambda x: STATE_COORDS.get(x, (None, None))[1])
map_data = state_risk.dropna(subset=["Lat", "Lon"]).copy()

def risk_zone(score):
    if score >= 75:
        return "Critical"
    if score >= 55:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"

map_data["Risk Zone"] = map_data["Avg_AI_Risk"].apply(risk_zone)
map_data["AI Recommendation"] = map_data.apply(
    lambda r: "Deploy recovery capacity immediately" if r["Avg_AI_Risk"] >= 75
    else "Increase carrier priority and monitor SLA" if r["Avg_AI_Risk"] >= 55
    else "Keep on active watch" if r["Avg_AI_Risk"] >= 35
    else "Normal flow",
    axis=1
)

critical = int((map_data["Risk Zone"] == "Critical").sum())
high = int((map_data["Risk Zone"] == "High").sum())
avg_map_risk = float(map_data["Avg_AI_Risk"].mean()) if len(map_data) else 0
total_map_shipments = int(map_data["Shipments"].sum()) if len(map_data) else 0

st.markdown(f"""
<div class="tactical-map-shell">
  <div class="tactical-map-head">
    <div>
      <div class="map-kicker">AI BOTTLENECK RADAR • LIVE COMMAND VIEW</div>
      <h2>Dynamic Route Heatmap Intelligence</h2>
      <p>Geographic risk, shipment density, delay pressure, and AI recommendations combined into one tactical logistics layer.</p>
    </div>
    <div class="map-live-badge"><span></span> LIVE PULSE</div>
  </div>
  <div class="map-stat-grid">
    <div class="map-stat"><small>Avg AI Risk</small><b>{avg_map_risk:.1f}%</b><em>network pressure</em></div>
    <div class="map-stat"><small>Mapped Shipments</small><b>{total_map_shipments:,}</b><em>active flow</em></div>
    <div class="map-stat"><small>High Risk Zones</small><b>{high}</b><em>watch markets</em></div>
    <div class="map-stat"><small>Critical Zones</small><b>{critical}</b><em>urgent escalation</em></div>
  </div>
</div>
""", unsafe_allow_html=True)

if len(map_data):
    # Offline, fast-rendering tactical geo map.
    # This replaces Densitymapbox/Scattermapbox so it does not need Mapbox tiles
    # and avoids Plotly colorbar compatibility errors on different versions.
    fig = go.Figure()

    hub_lat, hub_lon = 39.5, -98.35
    for _, r in map_data.sort_values("Avg_AI_Risk", ascending=False).head(8).iterrows():
        fig.add_trace(go.Scattergeo(
            lat=[hub_lat, r["Lat"]],
            lon=[hub_lon, r["Lon"]],
            mode="lines",
            line=dict(width=2, color="rgba(45,245,196,.35)"),
            hoverinfo="skip",
            showlegend=False
        ))

    fig.add_trace(go.Scattergeo(
        lat=map_data["Lat"],
        lon=map_data["Lon"],
        mode="markers",
        marker=dict(
            size=(map_data["Shipments"] / max(map_data["Shipments"].max(), 1) * 38 + 14),
            color=map_data["Avg_AI_Risk"],
            colorscale=[
                [0.00, "#00a3ff"],
                [0.40, "#2df5c4"],
                [0.70, "#ffb84d"],
                [1.00, "#ff3860"],
            ],
            opacity=0.90,
            line=dict(width=2, color="rgba(255,255,255,.85)"),
            colorbar=dict(
                title="AI Risk",
                tickfont=dict(color="#dcecff"),
                thickness=14,
                len=0.74
            )
        ),
        text=map_data.apply(lambda r:
            f"<b>{r['State/Province']}</b><br>"
            f"Risk Zone: {r['Risk Zone']}<br>"
            f"AI Risk Score: {r['Avg_AI_Risk']}%<br>"
            f"Shipments: {int(r['Shipments']):,}<br>"
            f"Delay Rate: {r['Delay_Rate']}%<br>"
            f"Avg Lead Time: {r['Avg_Lead_Time']} days<br>"
            f"Profit Signal: ${r['Profit']:,.0f}<br>"
            f"AI Recommendation: {r['AI Recommendation']}",
            axis=1
        ),
        hovertemplate="%{text}<extra></extra>",
        showlegend=False
    ))

    fig.update_geos(
        scope="usa",
        projection_type="albers usa",
        showland=True,
        landcolor="rgb(13, 22, 34)",
        showlakes=True,
        lakecolor="rgb(9, 16, 26)",
        subunitcolor="rgba(85,166,255,.30)",
        countrycolor="rgba(85,166,255,.30)",
        bgcolor="rgba(0,0,0,0)"
    )
    fig.update_layout(
        height=560,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.markdown('<div class="premium-map-frame">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        top_states = map_data.sort_values("Avg_AI_Risk", ascending=False).head(12)
        fig2 = px.bar(
            top_states.sort_values("Avg_AI_Risk"),
            x="Avg_AI_Risk",
            y="State/Province",
            orientation="h",
            color="Risk Zone",
            text="Avg_AI_Risk",
            title="AI Risk Leaderboard by State",
            color_discrete_map={
                "Low": "#00a3ff",
                "Medium": "#2df5c4",
                "High": "#ffb84d",
                "Critical": "#ff3860",
            }
        )
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig2.update_layout(
            template="plotly_dark",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="AI Risk Score",
            yaxis_title="",
            margin=dict(l=10, r=35, t=50, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        render_native_ai_escalation_feed(map_data)
else:
    st.info("No mapped state coordinates available for the tactical map.")

st.markdown("### ⚡ AI Recommendations")
for rec in ctx["recommendations"]:
    st.success("🤖 " + rec)

st.markdown("### 🚨 High-Risk Shipment Watchlist")
cols = ["Order ID", "Region", "State/Province", "Ship Mode", "Lead Time", "AI Risk Score", "AI Risk Level", "AI Recommendation", "Gross Profit"]
st.dataframe(view.sort_values("AI Risk Score", ascending=False)[cols].head(50), use_container_width=True, height=420)
st.download_button("⬇ Export AI Watchlist CSV", view.sort_values("AI Risk Score", ascending=False)[cols].to_csv(index=False), "ai_risk_watchlist.csv", "text/csv")

st.markdown("### 🧩 Enterprise Database Activity")
st.dataframe(ctx["activity"], use_container_width=True)