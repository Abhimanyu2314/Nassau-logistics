
import streamlit as st

def render_ai_escalation_feed():
    st.markdown("""
<style>
.fixed-feed-shell{border:1px solid rgba(45,245,196,.28);border-radius:28px;padding:24px;background:linear-gradient(145deg,rgba(9,18,32,.94),rgba(8,19,34,.82));box-shadow:0 24px 80px rgba(0,0,0,.42)}
.fixed-feed-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:20px}
.fixed-feed-head h2{margin:0!important;color:#f3fbff!important;font-size:34px!important}
.fixed-feed-head p{margin:7px 0 0 0!important;color:#9fb3c8!important}
.fixed-live{border:1px solid rgba(45,245,196,.32);border-radius:16px;padding:11px 15px;color:#2df5c4;background:rgba(45,245,196,.08);font-weight:900}
.fixed-alert{display:grid;grid-template-columns:90px 1.2fr 1fr 1fr 1fr 80px;gap:16px;align-items:center;border:1px solid rgba(86,166,255,.18);background:linear-gradient(135deg,rgba(10,22,38,.95),rgba(8,16,30,.88));border-radius:18px;padding:16px;margin-bottom:13px;position:relative;overflow:hidden}
.fixed-alert:before{content:"";position:absolute;left:0;top:0;bottom:0;width:6px;background:#ff3860;box-shadow:0 0 20px #ff3860}
.fixed-alert.warning:before{background:#ffbf4d;box-shadow:0 0 20px #ffbf4d}
.fixed-orb{width:66px;height:66px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid #ff3860;color:#ff5b6b;font-size:28px;background:rgba(255,56,96,.08)}
.warning .fixed-orb{border-color:#ffbf4d;color:#ffbf4d;background:rgba(255,191,77,.08)}
.fixed-badge{display:inline-block;padding:5px 9px;border-radius:6px;border:1px solid rgba(255,56,96,.34);background:rgba(255,56,96,.11);color:#ff5b6b;font-weight:950;font-size:12px;margin-bottom:7px}
.warning .fixed-badge{border-color:rgba(255,191,77,.34);background:rgba(255,191,77,.11);color:#ffbf4d}
.fixed-state{font-size:23px;color:#fff;font-weight:950}.fixed-region{color:#8fa6bd;font-weight:800;font-size:13px;margin-top:5px;text-transform:uppercase}
.fixed-label{color:#8fa6bd;font-size:12px;font-weight:950;letter-spacing:.08em;text-transform:uppercase;margin-bottom:7px}
.fixed-risk{color:#ff5b6b;font-size:28px;font-weight:950}.warning .fixed-risk{color:#ffbf4d}
.fixed-num{color:#f1fbff;font-size:26px;font-weight:950}.fixed-trend{color:#ff5b6b;font-size:19px;font-weight:950}.warning .fixed-trend{color:#ffbf4d}
.fixed-time{color:#9fb3c8;text-align:right;font-weight:800}
@media(max-width:950px){.fixed-alert{grid-template-columns:80px 1fr 1fr}}@media(max-width:650px){.fixed-alert{grid-template-columns:1fr}.fixed-time{text-align:left}}
</style>
<div class="fixed-feed-shell">
  <div class="fixed-feed-head">
    <div><h2>⚡ AI Escalation Feed</h2><p>Real-time high-risk logistics alerts prioritized by AI</p></div>
    <div class="fixed-live">● LIVE<br><small>Updated just now</small></div>
  </div>
  <div class="fixed-alert"><div class="fixed-orb">⚠</div><div><div class="fixed-badge">CRITICAL</div><div class="fixed-state">Connecticut</div><div class="fixed-region">Northeast Region</div></div><div><div class="fixed-label">Risk Score</div><div class="fixed-risk">87.9%</div></div><div><div class="fixed-label">Affected Shipments</div><div class="fixed-num">82</div></div><div><div class="fixed-label">Trend</div><div class="fixed-trend">↗ +12.4%</div></div><div class="fixed-time">2m ago ›</div></div>
  <div class="fixed-alert"><div class="fixed-orb">⚠</div><div><div class="fixed-badge">CRITICAL</div><div class="fixed-state">Louisiana</div><div class="fixed-region">South Central</div></div><div><div class="fixed-label">Risk Score</div><div class="fixed-risk">87.7%</div></div><div><div class="fixed-label">Affected Shipments</div><div class="fixed-num">42</div></div><div><div class="fixed-label">Trend</div><div class="fixed-trend">↗ +9.8%</div></div><div class="fixed-time">3m ago ›</div></div>
  <div class="fixed-alert"><div class="fixed-orb">⚠</div><div><div class="fixed-badge">CRITICAL</div><div class="fixed-state">South Carolina</div><div class="fixed-region">Southeast</div></div><div><div class="fixed-label">Risk Score</div><div class="fixed-risk">87.6%</div></div><div><div class="fixed-label">Affected Shipments</div><div class="fixed-num">42</div></div><div><div class="fixed-label">Trend</div><div class="fixed-trend">↗ +11.2%</div></div><div class="fixed-time">4m ago ›</div></div>
  <div class="fixed-alert"><div class="fixed-orb">⚠</div><div><div class="fixed-badge">CRITICAL</div><div class="fixed-state">Rhode Island</div><div class="fixed-region">Northeast</div></div><div><div class="fixed-label">Risk Score</div><div class="fixed-risk">87.6%</div></div><div><div class="fixed-label">Affected Shipments</div><div class="fixed-num">56</div></div><div><div class="fixed-label">Trend</div><div class="fixed-trend">↗ +10.7%</div></div><div class="fixed-time">5m ago ›</div></div>
  <div class="fixed-alert warning"><div class="fixed-orb">⚠</div><div><div class="fixed-badge">WARNING</div><div class="fixed-state">Ohio</div><div class="fixed-region">Midwest</div></div><div><div class="fixed-label">Risk Score</div><div class="fixed-risk">87.5%</div></div><div><div class="fixed-label">Affected Shipments</div><div class="fixed-num">469</div></div><div><div class="fixed-label">Trend</div><div class="fixed-trend">↗ +8.3%</div></div><div class="fixed-time">6m ago ›</div></div>
</div>
""", unsafe_allow_html=True)
