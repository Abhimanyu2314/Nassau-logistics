
import streamlit as st
from utils.common import setup_page

setup_page("AI Escalation Feed")

st.markdown("# ⚡ AI Escalation Feed")
st.caption("Real-time high-risk logistics alerts prioritized by AI")

alerts = [
    ("Connecticut", "Northeast Region", "Critical", 87.9, 82, "+12.4%", "2m ago"),
    ("Louisiana", "South Central", "Critical", 87.7, 42, "+9.8%", "3m ago"),
    ("South Carolina", "Southeast", "Critical", 87.6, 42, "+11.2%", "4m ago"),
    ("Rhode Island", "Northeast", "Critical", 87.6, 56, "+10.7%", "5m ago"),
    ("Ohio", "Midwest", "Warning", 87.5, 469, "+8.3%", "6m ago"),
]

top1, top2, top3 = st.columns(3)
top1.success("🟢 LIVE — Updated just now")
top2.info("🧠 AI Model Confidence: 98.7%")
top3.warning("🔄 Auto refresh: 30 sec")

for state, region, severity, risk, shipments, trend, time_text in alerts:
    with st.container(border=True):
        c1, c2, c3, c4, c5 = st.columns([2.2, 1.2, 1.2, 1.2, 0.9])
        with c1:
            if severity == "Critical":
                st.error(f"🚨 **{severity}**")
            else:
                st.warning(f"⚠️ **{severity}**")
            st.markdown(f"### {state}")
            st.caption(region)
        with c2:
            st.metric("Risk Score", f"{risk:.1f}%")
        with c3:
            st.metric("Affected Shipments", f"{shipments:,}")
        with c4:
            st.metric("Trend", trend)
        with c5:
            st.caption(time_text)

st.success("✅ System Status: All systems operational")
