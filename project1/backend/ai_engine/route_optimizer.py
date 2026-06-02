
import pandas as pd
import numpy as np

class RouteOptimizer:
    """Enterprise route optimizer simulation with deterministic scoring."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def lane_scorecard(self) -> pd.DataFrame:
        df = self.df.copy()
        if "Delayed" not in df.columns:
            df["Delayed"] = (df.get("Lead Time", 0) > 5).astype(int)
        lanes = df.groupby(["Region", "State/Province", "Ship Mode"], observed=True).agg(
            Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Delay_Rate=("Delayed", "mean"),
            Profit=("Gross Profit", "sum"),
            Avg_Risk=("AI Risk Score", "mean") if "AI Risk Score" in df.columns else ("Lead Time", "mean"),
        ).reset_index()
        lanes["Delay_Rate"] = lanes["Delay_Rate"] * 100
        lanes["Optimization_Score"] = (
            100
            - lanes["Avg_Lead_Time"].fillna(0) * 4
            - lanes["Delay_Rate"].fillna(0) * 0.45
            - lanes["Avg_Risk"].fillna(0) * 0.25
            + np.log1p(lanes["Profit"].clip(lower=0)) * 1.5
        ).clip(0, 100).round(1)
        lanes["Priority"] = pd.cut(lanes["Optimization_Score"], [-1, 45, 70, 100], labels=["Critical", "Watch", "Optimized"])
        return lanes.sort_values(["Priority", "Optimization_Score", "Shipments"], ascending=[True, True, False])

    def next_actions(self, top_n: int = 6):
        lanes = self.lane_scorecard().head(top_n)
        actions = []
        for _, r in lanes.iterrows():
            actions.append({
                "Lane": f"{r['Region']} → {r['State/Province']} / {r['Ship Mode']}",
                "Priority": str(r["Priority"]),
                "Action": "Escalate carrier review" if str(r["Priority"]) == "Critical" else "Monitor and rebalance capacity",
                "Optimization Score": float(r["Optimization_Score"]),
            })
        return pd.DataFrame(actions)
