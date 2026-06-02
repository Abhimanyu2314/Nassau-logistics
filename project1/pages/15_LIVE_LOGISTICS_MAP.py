import streamlit as st
from utils.common import setup_page
import plotly.graph_objects as go
import numpy as np
from utils.live_map_core import live_map_data, FAST_PLOTLY_CONFIG


@st.cache_resource(show_spinner=False)
def build_live_network_figure(routes_json, hubs_json):
    import pandas as pd
    import plotly.graph_objects as go
    routes = pd.read_json(routes_json)
    hubs = hubs_json
    fig = go.Figure()
    max_volume = max(float(routes.Volume.max()), 1.0)
    for _, r in routes.iterrows():
        color = "#ff3860" if r.Status == "Critical" else "#ffbf4d" if r.Status == "Watch" else "#2df5c4"
        width = 1.2 + (float(r.Volume) / max_volume) * 3.2
        fig.add_trace(go.Scattergeo(
            lon=[r.Origin_Lon, r.Dest_Lon],
            lat=[r.Origin_Lat, r.Dest_Lat],
            mode="lines",
            line=dict(width=width, color=color),
            opacity=0.38,
            hoverinfo="text",
            text=f"{r.Route_ID}<br>{r.Origin} → {r.Destination}<br>Risk: {r.Risk:.1f}%<br>Volume: {r.Volume}<br>ETA: {r.ETA:.1f}d<br>Status: {r.Status}",
            showlegend=False
        ))
    hub_names = list(hubs.keys())
    hub_lats = [hubs[h][0] for h in hub_names]
    hub_lons = [hubs[h][1] for h in hub_names]
    hub_volume, hub_risk = [], []
    for h in hub_names:
        sub = routes[(routes.Origin == h) | (routes.Destination == h)]
        hub_volume.append(int(sub.Volume.sum()))
        hub_risk.append(float(sub.Risk.mean()))
    max_hub_volume = max(hub_volume) if hub_volume else 1
    fig.add_trace(go.Scattergeo(
        lon=hub_lons,
        lat=hub_lats,
        text=[f"{h}<br>Volume: {v:,}<br>Risk: {risk:.1f}%" for h, v, risk in zip(hub_names, hub_volume, hub_risk)],
        mode="markers+text",
        marker=dict(
            size=[12 + v/max_hub_volume*22 for v in hub_volume],
            color=hub_risk,
            colorscale=[[0,"#2df5c4"],[.55,"#ffbf4d"],[1,"#ff3860"]],
            line=dict(width=1, color="white"),
            opacity=0.9
        ),
        textposition="top center",
        hovertemplate="%{text}<extra></extra>",
        showlegend=False
    ))
    fig.update_geos(scope="usa", projection_type="albers usa", showland=True, landcolor="rgb(9, 18, 31)", showocean=True, oceancolor="rgb(4, 8, 16)", lakecolor="rgb(4, 8, 16)", showlakes=True, showcountries=False, showsubunits=True, subunitcolor="rgba(120,170,220,.25)")
    fig.update_layout(template="plotly_dark", height=570, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, uirevision="live_map_cached")
    return fig

@st.cache_resource(show_spinner=False)
def build_risk_timeline_figure():
    import plotly.graph_objects as go
    import numpy as np
    rng = np.random.default_rng(212)
    x = list(range(1, 25))
    y = 45 + np.cumsum(rng.normal(0, 1.8, 24))
    fig2 = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color="#2df5c4", width=3), marker=dict(size=6)))
    fig2.update_layout(template="plotly_dark", height=285, margin=dict(l=10,r=10,t=0,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", uirevision="risk_timeline_cached")
    return fig2

setup_page("LIVE LOGISTICS MAP")

st.markdown("""
<style>
.stApp{
background:
radial-gradient(circle at 10% 8%,rgba(45,245,196,.15),transparent 28%),
radial-gradient(circle at 86% 14%,rgba(86,166,255,.13),transparent 32%),
linear-gradient(135deg,#040810,#07101b 55%,#050b12)!important;
}
.block-container{padding-top:.9rem!important;max-width:1680px!important}
.live-hero{
border:1px solid rgba(45,245,196,.34);
border-radius:36px;
padding:30px;
margin-bottom:16px;
background:linear-gradient(145deg,rgba(8,18,31,.98),rgba(8,34,37,.78));
box-shadow:0 18px 45px rgba(0,0,0,.36),inset 0 0 40px rgba(45,245,196,.04);
position:relative;
overflow:hidden;
}
.live-hero:before{
content:"";
position:absolute;
inset:-4px;
background:linear-gradient(115deg,transparent,rgba(45,245,196,.22),rgba(86,166,255,.12),transparent);
transform:translateX(-90%);
animation:scan 9s linear infinite;
}
@keyframes scan{100%{transform:translateX(90%)}} @keyframes pulse{50%{opacity:.45;transform:scale(.72)}}
.hero-row{position:relative;z-index:1;display:flex;justify-content:space-between;align-items:flex-start;gap:18px;flex-wrap:wrap}
.kicker{color:#2df5c4;font-size:12px;font-weight:950;letter-spacing:.18em}
.hero-row h1{font-size:60px!important;line-height:.98!important;letter-spacing:-.06em;margin:7px 0 8px 0!important;color:#f3fbff!important}
.hero-row p{color:#a9bacb!important;font-size:17px!important;margin:0!important;max-width:980px}
.live-pill{border:1px solid rgba(45,245,196,.38);background:rgba(45,245,196,.08);color:#2df5c4;border-radius:999px;padding:11px 15px;font-weight:950;display:flex;align-items:center;gap:9px}
.live-pill span{width:10px;height:10px;border-radius:50%;background:#2df5c4;box-shadow:0 0 20px #2df5c4;animation:pulse 1.2s infinite}
.metric-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:20px;position:relative;z-index:1}
.metric{border:1px solid rgba(86,166,255,.22);border-radius:23px;padding:17px;background:linear-gradient(145deg,rgba(12,23,38,.92),rgba(8,14,24,.80));box-shadow:0 17px 48px rgba(0,0,0,.30);transition:.12s ease}
.metric:hover{transform:translateY(-4px);border-color:rgba(45,245,196,.56);box-shadow:0 0 40px rgba(45,245,196,.13)}
.metric small{display:block;color:#94a8bb;text-transform:uppercase;letter-spacing:.11em;font-size:10px;font-weight:950}
.metric b{display:block;color:#fff;font-size:25px;line-height:1.2;margin-top:5px}
.metric em{display:block;color:#2df5c4;font-style:normal;font-size:12px;font-weight:800;margin-top:3px}
.panel{border:1px solid rgba(86,166,255,.22);border-radius:26px;padding:16px;background:rgba(9,17,28,.78);box-shadow:0 19px 58px rgba(0,0,0,.30)}
.panel h3{margin:0 0 12px 0!important;color:#f4fbff!important;font-size:19px!important}
.feed-card{border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.035);border-radius:16px;padding:12px;margin-bottom:9px}
.feed-card b{color:#fff}.feed-card small{color:#9fb3c8;display:block;margin-top:3px}
.footer{margin-top:16px;border:1px solid rgba(45,245,196,.20);background:rgba(45,245,196,.055);border-radius:18px;padding:14px;text-align:center;color:#2df5c4;font-weight:950}
@media(max-width:900px){.metric-grid{grid-template-columns:1fr 1fr}}
</style>
""", unsafe_allow_html=True)

routes, hubs = live_map_data()
critical = int((routes.Status == "Critical").sum())
watch = int((routes.Status == "Watch").sum())
avg_risk = routes.Risk.mean()
total_volume = int(routes.Volume.sum())

st.markdown(f"""
<div class="live-hero">
<div class="hero-row">
<div>
<div class="kicker">TITAN ENTERPRISE • PHASE 10 LIVE MAP</div>
<h1>Real-Time Logistics Map</h1>
<p>Interactive tactical route map with live shipment nodes, animated route arcs, AI risk heat signals, and operational command insights.</p>
</div>
<div class="live-pill"><span></span> LIVE MAP ACTIVE</div>
</div>
<div class="metric-grid">
<div class="metric"><small>Active Routes</small><b>{len(routes)}</b><em>live lanes</em></div>
<div class="metric"><small>Total Volume</small><b>{total_volume:,}</b><em>shipment pulse</em></div>
<div class="metric"><small>Avg Risk</small><b>{avg_risk:.1f}%</b><em>AI signal</em></div>
<div class="metric"><small>Critical Lanes</small><b>{critical}</b><em>urgent watch</em></div>
<div class="metric"><small>Watch Lanes</small><b>{watch}</b><em>monitoring</em></div>
</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1.55, 1])

with c1:
    st.markdown('<div class="panel"><h3>🌍 Live Tactical Route Network</h3>', unsafe_allow_html=True)
    fig = build_live_network_figure(routes.to_json(), hubs)
    st.plotly_chart(fig, use_container_width=True, config=FAST_PLOTLY_CONFIG)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel"><h3>⚡ Live Route Alerts</h3>', unsafe_allow_html=True)
    top = routes.sort_values("Risk", ascending=False).head(8)
    for _, r in top.iterrows():
        if r.Status == "Critical":
            st.error(f"🚨 **{r.Origin} → {r.Destination}** | Risk **{r.Risk:.1f}%** | Volume **{r.Volume}**")
        elif r.Status == "Watch":
            st.warning(f"⚠️ **{r.Origin} → {r.Destination}** | Risk **{r.Risk:.1f}%** | Volume **{r.Volume}**")
        else:
            st.info(f"✅ **{r.Origin} → {r.Destination}** | Risk **{r.Risk:.1f}%** | Volume **{r.Volume}**")
    st.success("🤖 AI Recommendation: redirect capacity from stable green lanes into the top 3 critical red lanes.")
    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns([1,1])

with c3:
    st.markdown('<div class="panel"><h3>📈 Route Risk Timeline</h3>', unsafe_allow_html=True)
    fig2 = build_risk_timeline_figure()
    st.plotly_chart(fig2, use_container_width=True, config=FAST_PLOTLY_CONFIG)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="panel"><h3>🧠 AI Command Actions</h3>', unsafe_allow_html=True)
    st.success("Optimize route capacity")
    st.info("Generate executive map report")
    st.warning("Monitor critical lanes")
    st.error("Escalate SLA breach routes")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">✓ Phase 10 complete • ✓ Real interactive logistics map • ✓ Live route alerts • ✓ AI tactical route intelligence</div>', unsafe_allow_html=True)