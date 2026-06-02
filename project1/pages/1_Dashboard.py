import streamlit as st
import plotly.express as px
from utils.common import v5_hyper_css, back_to_home_button, back_to_home_button, page_loader, brand_header, animated_download_button, animated_button, setup_page, hero, load_data, sidebar_filters, route_metrics, state_metrics, kpi_row, empty_guard, run_visible_steps, animated_success, shimmer_loading
setup_page("Dashboard")
v5_hyper_css()
page_loader("Opening 1 Dashboard")
brand_header()
hero("Executive Dashboard", "Main overview page for shipping route efficiency and operational performance.")
back_to_home_button()
with st.spinner("Loading optimized dashboard data..."):
    df = load_data()
df = sidebar_filters(df); empty_guard(df)
routes = route_metrics(df)
kpi_row(df, routes)


st.markdown("### Dashboard Processing")
if animated_button(
    "Run Dashboard Insights",
    key="run_dashboard_insights",
    steps=[
        ("Loading Dashboard Data", "Reading optimized shipment dataset."),
        ("Applying Filters", "Filtering selected route and state combinations."),
        ("Computing KPIs", "Calculating lead times, delays, and profits."),
        ("Generating Charts", "Rendering executive visual analytics.")
    ],
    success_message="Dashboard insights generated"
):
    run_visible_steps([
        ("Loaded Optimized Dataset", "Cached shipment data loaded successfully."),
        ("Applied Filters", "Selected date, region, state, ship mode, and factory filters applied."),
        ("Calculated KPIs", "Shipment count, lead time, delay rate, best route, and total profit calculated."),
        ("Generated Visual Insights", "Monthly trends, route ranking, and bottleneck snapshot prepared.")
    ])
    animated_success("Dashboard insights generated", "The dashboard results are visible below.")


st.markdown("### Performance Overview")
c1,c2 = st.columns([1.1,1])
with c1:
    top = routes.head(10).sort_values("Efficiency_Score")
    fig = px.bar(top, x="Efficiency_Score", y="Route", orientation="h", title="Top 10 Efficient Routes", color="Efficiency_Score", color_continuous_scale="Greens")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    ts = df.groupby("Month", as_index=False).agg(Orders=("Order ID","count"), Avg_Lead_Time=("Lead Time","mean"), Delay_Rate=("Delayed","mean"))
    fig = px.line(ts, x="Month", y="Orders", markers=True, title="Monthly Shipment Volume")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Bottleneck Snapshot")
bot = routes[(routes["Shipments"] >= routes["Shipments"].median())].sort_values(["Delay_Rate","Avg_Lead_Time"], ascending=False).head(10)
st.dataframe(bot[["Route","Shipments","Avg_Lead_Time","Delay_Rate","Efficiency_Score","Risk","Sales","Profit"]], use_container_width=True, hide_index=True)
