import streamlit as st
from backend.ai_engine.logistics_ai import LogisticsAIEngine
from backend.ai_engine.route_optimizer import RouteOptimizer
from database.db import initialize_database, read_activity, log_activity


@st.cache_data(show_spinner=False, ttl=86400)
def build_enterprise_context(df):
    """Cached enterprise context so Command Center / Neural Ops open fast.

    The old version rebuilt predictions and rewrote the SQLite table on every page load,
    which made all phases feel slow. This function now runs once per data change and
    reuses the computed result across pages.
    """
    engine = LogisticsAIEngine(df)
    scored = engine.add_predictions()
    optimizer = RouteOptimizer(scored)

    # Database writes are intentionally lightweight and cached with this function.
    initialize_database(scored)
    log_activity("PHASE_OPTIMIZED", "Cached enterprise AI command context loaded")

    return {
        "scored_shipments": scored,
        "summary": engine.kpi_summary(),
        "state_bottlenecks": engine.bottlenecks("State/Province", 12),
        "region_bottlenecks": engine.bottlenecks("Region", 8),
        "recommendations": engine.recommendations(),
        "lane_scorecard": optimizer.lane_scorecard(),
        "next_actions": optimizer.next_actions(),
        "activity": read_activity(15),
    }
