import streamlit as st
import plotly.express as px
from utils.common import (
    v5_hyper_css, back_to_home_button, page_loader, brand_header,
    animated_download_button, animated_button, setup_page, hero, load_data,
    sidebar_filters, route_metrics, kpi_row, empty_guard, run_visible_steps,
    animated_success, _ensure_nassau_route_columns
)

setup_page("Route Efficiency")
v5_hyper_css()
page_loader("Opening Route Efficiency")
brand_header()
hero(
    "Route Efficiency Results",
    "Top routes, bottom routes, route score, volume, delay frequency, profitability, and route drill-down."
)
back_to_home_button()

if animated_button(
    "Refresh route results",
    key="refresh_route_results",
    steps=[
        ("Refreshing Cache", "Clearing previous route computations."),
        ("Reloading Dataset", "Loading optimized shipment records."),
        ("Rebuilding Route Intelligence", "Generating fresh route efficiency insights."),
    ],
    success_message="Route results refreshed",
):
    st.cache_data.clear()
    st.success("Refresh completed. Results are updated on next interaction.")

df = sidebar_filters(load_data())
df = _ensure_nassau_route_columns(df)
empty_guard(df)
routes = route_metrics(df)
threshold = st.session_state.get("lead_time_threshold_days", int(df["Expected Lead Time"].median()))
routes["Threshold_Breach_Rate"] = routes["Route"].map(df.groupby("Route")["Lead Time"].apply(lambda s: (s > threshold).mean())).fillna(0)

kpi_row(df, routes)

st.markdown("### Run Route Intelligence")
if animated_button(
    "Generate Animated Route Analysis",
    key="step_route_analysis",
    steps=[
        ("Reading Shipment Data", "Preparing route-level shipment records."),
        ("Computing Route Metrics", "Calculating delay and lead time statistics."),
        ("Ranking Routes", "Generating efficiency score leaderboard."),
        ("Preparing Results", "Rendering bottlenecks and downloadable reports."),
    ],
    success_message="Route analysis completed",
):
    run_visible_steps([
        ("Data Filter Applied", "Filtered shipment records prepared for route analysis."),
        ("Route Metrics Calculated", "Average lead time, delay rate, shipment volume, profit, cost, and variability calculated."),
        ("Efficiency Score Generated", "Routes ranked using lead time, delay rate, consistency, and shipment volume."),
        ("Top and Bottom Routes Identified", "Most efficient and least efficient routes are ready below."),
    ])
    animated_success("Route analysis completed", "Scroll down to view leaderboard, bottlenecks, drill-down, and downloadable results.")

show_cols = ["Route", "Shipments", "Avg_Lead_Time", "Lead_Std", "Delay_Rate", "Threshold_Breach_Rate", "Efficiency_Score", "Sales", "Profit", "Cost", "Risk"]
show_cols = [c for c in show_cols if c in routes.columns]

c1, c2 = st.columns(2)
with c1:
    st.markdown("### ✅ Top 10 Most Efficient Routes")
    st.dataframe(routes.head(10)[show_cols], use_container_width=True, hide_index=True)
with c2:
    st.markdown("### ⚠️ Bottom 10 Least Efficient Routes")
    st.dataframe(routes.sort_values("Efficiency_Score").head(10)[show_cols], use_container_width=True, hide_index=True)

st.markdown("### Route Efficiency Leaderboard")
fig = px.scatter(
    routes,
    x="Avg_Lead_Time",
    y="Delay_Rate",
    size="Shipments",
    color="Efficiency_Score",
    hover_name="Route",
    color_continuous_scale="RdYlGn",
    title="Lead Time vs Delay Rate by Route",
)
fig.update_layout(template="plotly_dark", height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Route Drill-Down")
selected_route = st.selectbox("Select a factory-to-customer route", routes["Route"].tolist(), key="route_drilldown_select")
drill = df[df["Route"] == selected_route].copy()
if len(drill):
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Orders", f"{len(drill):,}")
    d2.metric("Avg Lead Time", f"{drill['Lead Time'].mean():.1f} days")
    d3.metric("Threshold Breach", f"{(drill['Lead Time'] > threshold).mean()*100:.1f}%")
    d4.metric("Gross Profit", f"${drill['Gross Profit'].sum():,.0f}")

    timeline_cols = ["Order ID", "Order Date", "Ship Date", "Ship Mode", "City", "State/Province", "Region", "Product Name", "Lead Time", "Delayed", "Sales", "Gross Profit", "Cost", "Units"]
    timeline_cols = [c for c in timeline_cols if c in drill.columns]
    st.dataframe(drill.sort_values("Order Date", ascending=False)[timeline_cols].head(250), use_container_width=True, hide_index=True)

    timeline = drill.groupby("Order Date", as_index=False).agg(Shipments=("Order ID", "count"), Avg_Lead_Time=("Lead Time", "mean"))
    fig2 = px.line(timeline, x="Order Date", y="Avg_Lead_Time", markers=True, title="Order-Level Shipment Timeline")
    fig2.update_layout(template="plotly_dark", height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

animated_download_button("route efficiency results", routes.to_csv(index=False).encode(), "route_efficiency_results.csv", "text/csv", key="route_efficiency_download")

st.markdown("### Factory → Customer Region Leaderboard")
df = _ensure_nassau_route_columns(df)
region_routes = df.groupby("Factory → Customer Region", observed=True, dropna=False).agg(
    Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean"),
    Lead_Time_Variability=("Lead Time", "std"),
    Delay_Frequency=("Delayed", "mean"),
    Sales=("Sales", "sum"),
    Profit=("Gross Profit", "sum"),
).reset_index()
region_routes["Lead_Time_Variability"] = region_routes["Lead_Time_Variability"].fillna(0)
# Simple regional score for requirement-level factory-to-region analysis.
def _rr_norm(s):
    rng = s.max() - s.min()
    return (s - s.min()) / rng if rng else s * 0
region_routes["Region_Efficiency_Score"] = (100 - (0.55*_rr_norm(region_routes["Avg_Lead_Time"]) + 0.35*region_routes["Delay_Frequency"] + 0.10*_rr_norm(region_routes["Lead_Time_Variability"])) * 100).clip(0, 100).round(1)
region_routes["Delay_Frequency_%"] = (region_routes["Delay_Frequency"] * 100).round(1)
st.dataframe(region_routes.sort_values("Region_Efficiency_Score", ascending=False), use_container_width=True, hide_index=True)

st.markdown("### Requirement KPI Definitions")
st.markdown("""
- **Shipping Lead Time:** `Ship Date − Order Date`
- **Average Lead Time:** mean shipping duration per factory-to-customer route
- **Route Volume:** number of orders/shipments per route
- **Delay Frequency:** percent of shipments exceeding selected/expected threshold
- **Route Efficiency Score:** normalized route score using lead time, delay rate, variability, and operational exposure
""")
