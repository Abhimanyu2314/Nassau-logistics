import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.common import v5_hyper_css, back_to_home_button, back_to_home_button, page_loader, brand_header, animated_download_button, animated_button, setup_page, hero, load_data, sidebar_filters, state_metrics, route_metrics, FACTORIES, empty_guard, run_visible_steps, animated_success, shimmer_loading
setup_page("Geographic Analysis")
v5_hyper_css()
page_loader("Opening 3 Geographic Analysis")
brand_header()
hero("Geographic Shipping Results", "Expected result page: state heatmap, regional bottlenecks, and factory-to-state route visualization.")
back_to_home_button()
df = sidebar_filters(load_data()); empty_guard(df)
states = state_metrics(df)
routes = route_metrics(df)


st.markdown("### Geographic Processing")
if animated_button(
    "Generate Map Analysis",
    key="run_geo_steps",
    steps=[
        ("Preparing Geographic Data", "Loading state and factory coordinates."),
        ("Computing Bottlenecks", "Detecting congestion-prone regions."),
        ("Building Route Network", "Creating shipment route paths."),
        ("Rendering Maps", "Generating heatmaps and route visualizations.")
    ],
    success_message="Map analysis completed"
):
    run_visible_steps([
        ("State Metrics Prepared", "Average lead time and delay rate calculated by state."),
        ("Factory Coordinates Loaded", "Factory latitude and longitude points mapped."),
        ("Route Lines Generated", "Factory-to-state shipment connections prepared for visualization."),
        ("Bottleneck Hotspots Identified", "High lead-time states and congested routes highlighted.")
    ])
    animated_success("Geographic analysis completed", "Maps and route lines are shown below.")


c1,c2,c3 = st.columns(3)
c1.metric("States Served", states["State/Province"].nunique())
c2.metric("Worst State Lead Time", f"{states['Avg_Lead_Time'].max():.1f} days")
c3.metric("Highest State Delay", f"{states['Delay_Rate'].max()*100:.1f}%")

st.markdown("### US Shipping Efficiency Heatmap")
fig = go.Figure(go.Choropleth(locations=states["State_Code"], z=states["Avg_Lead_Time"], locationmode="USA-states", colorscale="Reds", colorbar_title="Avg Lead Time", text=states["State/Province"]))
fig.update_layout(template="plotly_dark", geo_scope="usa", height=520, paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Factory-to-State Route Map")
fig = go.Figure()
for f, info in FACTORIES.items():
    fig.add_trace(go.Scattergeo(lon=[info['lon']], lat=[info['lat']], text=[f], mode='markers+text', marker=dict(size=13, color='#29d391'), name=f))
for _, r in routes.dropna(subset=["Factory_Lon","Factory_Lat","State_Lon","State_Lat"]).head(80).iterrows():
    fig.add_trace(go.Scattergeo(lon=[r.Factory_Lon, r.State_Lon], lat=[r.Factory_Lat, r.State_Lat], mode='lines', line=dict(width=max(1, r.Shipments/routes.Shipments.max()*5), color='rgba(41,211,145,.35)'), showlegend=False, hoverinfo='skip'))
fig.update_layout(template="plotly_dark", geo_scope="usa", height=560, paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Regional Bottleneck Table")
st.dataframe(states.sort_values(["Delay_Rate","Avg_Lead_Time"], ascending=False), use_container_width=True, hide_index=True)

st.markdown("### Regional Bottleneck Visualization")
region_bottlenecks = df.groupby("Region", observed=True).agg(
    Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean"),
    Delay_Rate=("Delayed", "mean"),
    Sales=("Sales", "sum"),
    Profit=("Gross Profit", "sum"),
).reset_index()
region_bottlenecks["Delay_Frequency_%"] = (region_bottlenecks["Delay_Rate"] * 100).round(1)
fig = px.scatter(
    region_bottlenecks,
    x="Shipments",
    y="Avg_Lead_Time",
    size="Delay_Rate",
    color="Delay_Rate",
    hover_name="Region",
    title="Regional bottlenecks: high shipment volume + poor lead-time performance",
    color_continuous_scale="Reds",
)
fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(region_bottlenecks.sort_values(["Delay_Rate", "Avg_Lead_Time", "Shipments"], ascending=False), use_container_width=True, hide_index=True)
