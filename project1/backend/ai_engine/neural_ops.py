import pandas as pd
import numpy as np

class NeuralOpsEngine:
    """Phase 4 enterprise intelligence layer for predictive logistics simulation."""

    def __init__(self, scored_df: pd.DataFrame):
        self.df = scored_df.copy()

    def control_tower_summary(self) -> dict:
        df = self.df
        active = int(len(df))
        high = int((df.get("AI Risk Score", 0) >= 70).sum())
        critical_pct = round((high / active * 100), 1) if active else 0
        profit = float(df.get("Gross Profit", pd.Series(dtype=float)).sum())
        return {
            "active_shipments": active,
            "critical_shipments": high,
            "critical_percent": critical_pct,
            "network_health": max(0, round(100 - critical_pct - float(df.get("Delayed", pd.Series([0])).mean() * 35), 1)),
            "profit_protected": round(profit * (1 - critical_pct / 100), 2),
        }

    def mission_timeline(self) -> pd.DataFrame:
        df = self.df.copy()
        if "Order Date" in df.columns:
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
            key = df["Order Date"].dt.to_period("M").astype(str)
        else:
            key = pd.Series(np.arange(len(df)) // max(1, len(df)//12), index=df.index).astype(str)
        out = df.groupby(key, observed=True).agg(
            Shipments=("Order ID", "count"),
            Avg_Risk=("AI Risk Score", "mean"),
            Delays=("Delayed", "sum"),
            Profit=("Gross Profit", "sum"),
        ).reset_index(names="Period")
        out["Neural_Load"] = (out["Shipments"] * (out["Avg_Risk"].fillna(0) / 100)).round(1)
        return out

    def fleet_watch(self, top_n=20) -> pd.DataFrame:
        cols = [c for c in ["Order ID", "Region", "State/Province", "Ship Mode", "Lead Time", "Gross Profit", "AI Risk Score", "AI Risk Level", "AI Recommendation"] if c in self.df.columns]
        out = self.df.sort_values("AI Risk Score", ascending=False)[cols].head(top_n).copy()
        out["Ops_Status"] = np.select(
            [out["AI Risk Score"] >= 80, out["AI Risk Score"] >= 60],
            ["RED ALERT", "ACTIVE WATCH"],
            default="NORMAL"
        )
        return out

    def regional_radar(self) -> pd.DataFrame:
        out = self.df.groupby("Region", observed=True).agg(
            Shipments=("Order ID", "count"),
            Avg_Risk=("AI Risk Score", "mean"),
            Delay_Rate=("Delayed", "mean"),
            Profit=("Gross Profit", "sum"),
        ).reset_index()
        out["Delay_Rate"] = (out["Delay_Rate"] * 100).round(1)
        out["Command_Status"] = pd.cut(out["Avg_Risk"], [-1, 40, 65, 100], labels=["Stable", "Watch", "Critical"])
        return out.sort_values("Avg_Risk", ascending=False)

    def ai_briefing(self) -> list[str]:
        summary = self.control_tower_summary()
        radar = self.regional_radar()
        worst_region = radar.iloc[0]["Region"] if len(radar) else "Unknown"
        return [
            f"Network health is {summary['network_health']}%. Keep priority lanes under continuous monitoring.",
            f"{summary['critical_shipments']} shipments are in critical AI-risk state.",
            f"Highest pressure region: {worst_region}. Allocate tactical review capacity there first.",
            "Use the fleet watch table to export RED ALERT shipments for immediate dispatch action.",
        ]
