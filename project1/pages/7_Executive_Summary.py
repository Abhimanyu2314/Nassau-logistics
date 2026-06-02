import streamlit as st
from utils.common import v5_hyper_css, back_to_home_button, back_to_home_button, page_loader, brand_header, animated_download_button, animated_button, setup_page, hero, load_data, sidebar_filters, route_metrics, state_metrics, empty_guard
setup_page("Executive Summary")
v5_hyper_css()
page_loader("Opening 7 Executive Summary")
brand_header()
hero("Executive Summary Results", "Expected result page: stakeholder-ready conclusion, insights, bottlenecks, and recommendations.")
back_to_home_button()
df = sidebar_filters(load_data()); empty_guard(df)
routes = route_metrics(df); states = state_metrics(df)
best = routes.iloc[0]; worst = routes.sort_values('Efficiency_Score').iloc[0]
worst_state = states.sort_values(['Delay_Rate','Avg_Lead_Time'], ascending=False).iloc[0]

st.markdown("### Summary")
st.markdown(f"""
<div class='card'>
<p>Nassau Candy Distributor processed <b>{len(df):,}</b> shipments in the selected view. The average shipping lead time is <b>{df['Lead Time'].mean():.1f} days</b>, with a delay frequency of <b>{df['Delayed'].mean()*100:.1f}%</b>.</p>
<p>The best performing route is <b>{best['Route']}</b> with an efficiency score of <b>{best['Efficiency_Score']}</b>. The lowest performing route is <b>{worst['Route']}</b> with an efficiency score of <b>{worst['Efficiency_Score']}</b>.</p>
<p>The most critical geographic bottleneck is <b>{worst_state['State/Province']}</b>, showing <b>{worst_state['Delay_Rate']*100:.1f}%</b> delay rate.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
1. Prioritize operational review for **{worst['Route']}** because it has the weakest route score.
2. Investigate state-level delivery constraints in **{worst_state['State/Province']}**.
3. Compare ship modes on high-volume routes before changing delivery policies.
4. Use the AI Prediction page to test future shipment scenarios before dispatch planning.
5. Track efficiency score monthly to move from reactive logistics to proactive optimization.
""")







st.markdown("### Government / Stakeholder Executive Brief")
st.markdown(f"""
<div class='card'>
<h4>Key Findings</h4>
<ul>
<li>Current filtered operations include <b>{len(df):,}</b> shipments across <b>{routes['Route'].nunique():,}</b> factory-to-customer state routes.</li>
<li>Average lead time is <b>{df['Lead Time'].mean():.1f} days</b>, and delay frequency is <b>{df['Delayed'].mean()*100:.1f}%</b>.</li>
<li>The most efficient lane is <b>{best['Route']}</b>; the highest-priority recovery lane is <b>{worst['Route']}</b>.</li>
</ul>
<h4>Operational Risks</h4>
<ul>
<li>High-volume routes with poor lead time create customer-service risk and reduce scalability.</li>
<li>Regions with high delay frequency should be monitored as geographic bottlenecks.</li>
<li>Ship-mode decisions should consider both time performance and profit impact.</li>
</ul>
<h4>Recommendations</h4>
<ul>
<li>Prioritize corrective action for <b>{worst['Route']}</b> and states with the highest delay frequency.</li>
<li>Use expedited modes only on routes where delay reduction justifies the cost-time tradeoff.</li>
<li>Track Route Efficiency Score monthly and review bottom 10 routes as an operational routine.</li>
</ul>
<h4>Expected Impact</h4>
<ul>
<li>Improved delivery reliability, faster bottleneck detection, and more data-driven logistics planning.</li>
<li>Reduced reactive decision-making through route-level operational intelligence.</li>
</ul>
</div>
""", unsafe_allow_html=True)

summary_md = f"""# Executive Summary - Nassau Candy Distributor\n\nShipments analyzed: {len(df):,}\nAverage lead time: {df['Lead Time'].mean():.1f} days\nDelay frequency: {df['Delayed'].mean()*100:.1f}%\nBest route: {best['Route']}\nRecovery route: {worst['Route']}\nCritical state bottleneck: {worst_state['State/Province']}\n\nRecommendations:\n1. Review weakest route: {worst['Route']}\n2. Investigate geographic bottleneck: {worst_state['State/Province']}\n3. Compare ship modes by delay frequency and business impact\n4. Track route efficiency monthly\n"""
animated_download_button("executive summary markdown", summary_md.encode(), "executive_summary_nassau.md", "text/markdown", key="executive_summary_download_final")
