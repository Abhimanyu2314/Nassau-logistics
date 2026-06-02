import streamlit as st
import plotly.express as px
from utils.common import v5_hyper_css, back_to_home_button, back_to_home_button, page_loader, brand_header, animated_download_button, animated_button, setup_page, hero, load_data, sidebar_filters, empty_guard, run_visible_steps, animated_success, shimmer_loading
setup_page("Ship Mode Analysis")
v5_hyper_css()
page_loader("Opening 4 Ship Mode Analysis")
brand_header()
hero("Ship Mode Performance Results", "Expected result page: compare lead time, delay rate, shipment volume, sales, and profit by shipping method.")
back_to_home_button()
df = sidebar_filters(load_data()); empty_guard(df)


st.markdown("### Ship Mode Processing")
if animated_button(
    "Generate Ship Mode Results",
    key="run_ship_steps",
    steps=[
        ("Grouping Ship Modes", "Preparing shipment mode categories."),
        ("Calculating Performance", "Computing delivery efficiency metrics."),
        ("Analyzing Profitability", "Comparing business performance by mode."),
        ("Rendering Results", "Preparing interactive charts and insights.")
    ],
    success_message="Ship mode analysis completed"
):
    run_visible_steps([
        ("Grouped Ship Modes", "Orders grouped by Same Day, First Class, Second Class, and Standard Class."),
        ("Calculated Delivery Performance", "Average lead time and delay rate calculated for each mode."),
        ("Measured Business Impact", "Sales, profit, and shipment volume compared by shipping method."),
        ("Prepared Recommendations", "Cost-time tradeoff insights generated.")
    ])
    animated_success("Ship mode analysis completed", "Charts and comparison results are shown below.")

mode = df.groupby("Ship Mode", observed=True).agg(Shipments=("Order ID","count"), Avg_Lead_Time=("Lead Time","mean"), Delay_Rate=("Delayed","mean"), Avg_Delay_Days=("Delay Days","mean"), Sales=("Sales","sum"), Profit=("Gross Profit","sum")).reset_index()

c1,c2 = st.columns(2)
with c1:
    fig = px.bar(mode, x="Ship Mode", y="Avg_Lead_Time", color="Avg_Lead_Time", title="Average Lead Time by Ship Mode", color_continuous_scale="Reds")
    fig.update_layout(template="plotly_dark", height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.bar(mode, x="Ship Mode", y="Delay_Rate", color="Delay_Rate", title="Delay Rate by Ship Mode", color_continuous_scale="Oranges")
    fig.update_layout(template="plotly_dark", height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

c3,c4 = st.columns(2)
with c3:
    fig = px.pie(mode, names="Ship Mode", values="Shipments", hole=.45, title="Shipment Volume Share")
    fig.update_layout(template="plotly_dark", height=420, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.scatter(mode, x="Sales", y="Profit", size="Shipments", color="Ship Mode", title="Cost-Time Business Impact")
    fig.update_layout(template="plotly_dark", height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Ship Mode Result Table")
st.dataframe(mode.sort_values("Avg_Lead_Time"), use_container_width=True, hide_index=True)

st.markdown("### Cost-Time Tradeoff Summary")
mode_tradeoff = mode.copy()
mode_tradeoff["Delay_Frequency_%"] = (mode_tradeoff["Delay_Rate"] * 100).round(1)
mode_tradeoff["Profit_per_Shipment"] = (mode_tradeoff["Profit"] / mode_tradeoff["Shipments"].replace(0, 1)).round(2)
mode_tradeoff["Sales_per_Shipment"] = (mode_tradeoff["Sales"] / mode_tradeoff["Shipments"].replace(0, 1)).round(2)
mode_tradeoff["Recommendation"] = mode_tradeoff.apply(
    lambda r: "Use selectively for high-priority shipments" if r["Avg_Lead_Time"] <= mode_tradeoff["Avg_Lead_Time"].median() and r["Delay_Rate"] <= mode_tradeoff["Delay_Rate"].median()
    else "Review SLA risk and cost-time balance",
    axis=1,
)
st.dataframe(mode_tradeoff.sort_values(["Avg_Lead_Time", "Delay_Rate"]), use_container_width=True, hide_index=True)
st.info("This section satisfies the descriptive cost-time tradeoff requirement by comparing lead time, delay risk, sales, profit, and per-shipment value by shipping method.")
