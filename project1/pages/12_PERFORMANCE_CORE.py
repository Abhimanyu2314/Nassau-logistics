
import streamlit as st
from utils.common import setup_page
import numpy as np
import plotly.graph_objects as go
from utils.performance_core import generate_ops_data, FAST_PLOTLY_CONFIG, inject_speed_css

setup_page("PERFORMANCE CORE")
inject_speed_css()

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 12% 8%,rgba(45,245,196,.15),transparent 26%),radial-gradient(circle at 88% 14%,rgba(86,166,255,.12),transparent 30%),linear-gradient(135deg,#040810,#07101b 55%,#050b12)!important}
.block-container{padding-top:.9rem!important;max-width:1660px!important}
.core-hero{border:1px solid rgba(45,245,196,.32);border-radius:34px;padding:28px;margin-bottom:15px;background:radial-gradient(circle at 22% 18%,rgba(45,245,196,.10),transparent 28%),linear-gradient(145deg,rgba(8,18,31,.97),rgba(8,32,35,.76));box-shadow:0 26px 95px rgba(0,0,0,.46),inset 0 0 75px rgba(45,245,196,.05);position:relative;overflow:hidden}
.core-hero:before{content:"";position:absolute;inset:-4px;background:linear-gradient(115deg,transparent,rgba(45,245,196,.20),rgba(86,166,255,.12),transparent);transform:translateX(-88%);animation:scan 5.2s linear infinite}
@keyframes scan{100%{transform:translateX(88%)}} @keyframes pulse{50%{opacity:.45;transform:scale(.72)}}
.hero-row{position:relative;z-index:1;display:flex;justify-content:space-between;align-items:flex-start;gap:18px;flex-wrap:wrap}
.kicker{color:#2df5c4;font-size:12px;font-weight:950;letter-spacing:.18em}
.hero-row h1{font-size:58px!important;line-height:.98!important;letter-spacing:-.06em;margin:7px 0 8px 0!important;color:#f3fbff!important}
.hero-row p{color:#a9bacb!important;font-size:17px!important;margin:0!important;max-width:980px}
.live{border:1px solid rgba(45,245,196,.38);background:rgba(45,245,196,.08);color:#2df5c4;border-radius:999px;padding:11px 15px;font-weight:950;display:flex;align-items:center;gap:9px}
.live span{width:10px;height:10px;border-radius:50%;background:#2df5c4;box-shadow:0 0 20px #2df5c4;animation:pulse 1.2s infinite}
.metric-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-top:20px;position:relative;z-index:1}
.metric{border:1px solid rgba(86,166,255,.22);border-radius:22px;padding:16px;background:linear-gradient(145deg,rgba(12,23,38,.92),rgba(8,14,24,.80));box-shadow:0 16px 45px rgba(0,0,0,.28);transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease}
.metric:hover{transform:translateY(-3px);border-color:rgba(45,245,196,.52);box-shadow:0 0 36px rgba(45,245,196,.11)}
.metric small{display:block;color:#94a8bb;text-transform:uppercase;letter-spacing:.11em;font-size:10px;font-weight:950}
.metric b{display:block;color:#fff;font-size:25px;line-height:1.2;margin-top:5px}
.metric em{display:block;color:#2df5c4;font-style:normal;font-size:12px;font-weight:800;margin-top:3px}
.panel{border:1px solid rgba(86,166,255,.22);border-radius:25px;padding:16px;background:rgba(9,17,28,.76);box-shadow:0 18px 55px rgba(0,0,0,.28)}
.panel h3{margin:0 0 12px 0!important;color:#f4fbff!important;font-size:19px!important}
.command-strip{margin:14px 0;border:1px solid rgba(45,245,196,.24);background:linear-gradient(135deg,rgba(45,245,196,.075),rgba(86,166,255,.04));border-radius:22px;padding:15px 18px;color:#dffcf6;font-weight:900}
.command-strip small{display:block;color:#a2b3c3;font-weight:800;margin-top:4px}
.feed{display:flex;gap:12px;align-items:center;padding:12px;border-radius:16px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.075);margin-bottom:9px}
.feed span{width:10px;height:10px;border-radius:50%;background:#2df5c4;box-shadow:0 0 18px #2df5c4}
.feed.warn span{background:#ffbf4d;box-shadow:0 0 18px #ffbf4d}.feed.crit span{background:#ff3860;box-shadow:0 0 18px #ff3860}
.feed b{color:#fff}.feed small{display:block;color:#9fb3c8;margin-top:2px}
.action-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.action{border:1px solid rgba(45,245,196,.24);background:rgba(45,245,196,.075);color:#eafff9;border-radius:18px;padding:14px;font-weight:950;text-align:center;transition:.16s ease}
.action:hover{transform:scale(1.02);box-shadow:0 0 26px rgba(45,245,196,.12)}
.footer{margin-top:16px;border:1px solid rgba(45,245,196,.20);background:rgba(45,245,196,.055);border-radius:18px;padding:14px;text-align:center;color:#2df5c4;font-weight:950}
@media(max-width:1150px){.metric-grid{grid-template-columns:1fr 1fr 1fr}}
@media(max-width:650px){.metric-grid,.action-grid{grid-template-columns:1fr}.hero-row h1{font-size:38px!important}}
</style>
""", unsafe_allow_html=True)

df = generate_ops_data(seed=208, n=760)
hub_mode = df.groupby(["Hub", "Mode"], observed=True).agg(Risk=("AI_Risk","mean")).reset_index()
state_rank = df.groupby("State", observed=True).agg(Risk=("AI_Risk","mean"), Volume=("Volume","sum"), SLA=("SLA","mean")).sort_values("Risk", ascending=False).head(7)
route_eff = df.groupby("Route", observed=True).agg(Eff=("Profit","mean")).sort_values("Eff", ascending=False).head(7)

st.markdown(f"""
<div class="core-hero"><div class="hero-row"><div><div class="kicker">TITAN ENTERPRISE • PHASE 8 PERFORMANCE CORE</div><h1>PERFORMANCE CORE</h1><p>Smooth enterprise upgrade with faster page loading, cached analytics, reduced blocking effects, stabilized charts, and bug-safe command-center UI.</p></div><div class="live"><span></span> FAST MODE ACTIVE</div></div>
<div class="metric-grid">
<div class="metric"><small>Network Volume</small><b>{int(df.Volume.sum()):,}</b><em>cached flow</em></div>
<div class="metric"><small>AI Risk</small><b>{df.AI_Risk.mean():.1f}%</b><em>risk index</em></div>
<div class="metric"><small>Delay Load</small><b>{df.Delay.mean():.1f}%</b><em>SLA pressure</em></div>
<div class="metric"><small>SLA Health</small><b>{df.SLA.mean():.1f}%</b><em>delivery quality</em></div>
<div class="metric"><small>Profit Signal</small><b>${df.Profit.sum()/1000000:.2f}M</b><em>financial pulse</em></div>
<div class="metric"><small>Avg ETA</small><b>{df.ETA.mean():.1f}d</b><em>forecast</em></div>
</div></div>
""", unsafe_allow_html=True)

st.markdown("""<div class="command-strip">⚡ Efficiency Patch Applied
<small>Heavy loaders reduced, Plotly colorbar bug patched, chart modebars disabled, reusable cached data layer added, and new smooth fast command page introduced.</small></div>""", unsafe_allow_html=True)

c1, c2 = st.columns([1.45, 1])
with c1:
    st.markdown('<div class="panel"><h3>🧬 Smooth AI Risk Matrix</h3>', unsafe_allow_html=True)
    pivot = hub_mode.pivot(index="Hub", columns="Mode", values="Risk").fillna(0)
    fig = go.Figure(go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale=[[0,"#053b75"],[.42,"#2df5c4"],[.70,"#ffbf4d"],[1,"#ff3860"]], colorbar=dict(title=dict(text="Risk", font=dict(color="#dcecff")), tickfont=dict(color="#dcecff")), hovertemplate="<b>%{y}</b><br>Mode: %{x}<br>Risk: %{z:.1f}%<extra></extra>"))
    fig.update_layout(template="plotly_dark", height=390, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config=FAST_PLOTLY_CONFIG)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    items = ""
    for state, row in state_rank.iterrows():
        cls = "crit" if row.Risk > 58 else "warn" if row.Risk > 45 else ""
        items += f'<div class="feed {cls}"><span></span><div><b>{state}</b><small>{row.Risk:.1f}% risk • {int(row.Volume):,} volume • SLA {row.SLA:.1f}%</small></div></div>'
    st.markdown(f'<div class="panel"><h3>🚨 Optimized Escalation Feed</h3>{items}</div>', unsafe_allow_html=True)

c3, c4, c5 = st.columns(3)
with c3:
    st.markdown('<div class="panel"><h3>📈 Smooth Delivery Forecast</h3>', unsafe_allow_html=True)
    rng = np.random.default_rng(44); x = np.arange(1,25); y = 91 + np.cumsum(rng.normal(0, .65, 24))
    fig2 = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color="#2df5c4", width=3), marker=dict(size=6)))
    fig2.update_layout(template="plotly_dark", height=280, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True, config=FAST_PLOTLY_CONFIG)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="panel"><h3>🛰 Fast Route Efficiency</h3>', unsafe_allow_html=True)
    fig3 = go.Figure(go.Bar(x=route_eff.Eff, y=route_eff.index, orientation="h", marker=dict(color="#2df5c4")))
    fig3.update_layout(template="plotly_dark", height=280, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True, config=FAST_PLOTLY_CONFIG)
    st.markdown('</div>', unsafe_allow_html=True)

with c5:
    st.markdown("""<div class="panel"><h3>🛠 Bug Fix Command Dock</h3><div class="action-grid">
    <div class="action">Fast Load</div><div class="action">Cache Data</div><div class="action">Fix Plotly</div><div class="action">Smooth UI</div><div class="action">Reduce Lag</div><div class="action">Stable Charts</div>
    </div></div><div class="footer">✓ Phase 8 complete • ✓ Efficiency upgraded • ✓ Bugs patched • ✓ Smooth command UX</div>""", unsafe_allow_html=True)
