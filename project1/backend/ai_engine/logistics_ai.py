
import pandas as pd
import numpy as np

EXPECTED_DAYS = {"Same Day": 1, "First Class": 3, "Second Class": 5, "Standard Class": 7}

class LogisticsAIEngine:
    """Lightweight AI-style analytics engine for enterprise logistics intelligence."""

    def __init__(self, df: pd.DataFrame):
        self.df = self._prepare(df.copy())

    def _prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in ["Order Date", "Ship Date"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        if "Lead Time" not in df.columns and {"Order Date", "Ship Date"}.issubset(df.columns):
            df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days.clip(lower=0)
        df["Expected Lead"] = df["Ship Mode"].map(EXPECTED_DAYS).fillna(7)
        df["Delay Days"] = (df["Lead Time"] - df["Expected Lead"]).clip(lower=0)
        df["Delayed"] = (df["Delay Days"] > 0).astype(int)
        if "Gross Profit" in df.columns and "Sales" in df.columns:
            df["Profit Margin"] = np.where(df["Sales"].replace(0, np.nan).notna(), df["Gross Profit"] / df["Sales"].replace(0, np.nan), 0)
        else:
            df["Profit Margin"] = 0
        return df

    def risk_score(self, row: pd.Series) -> int:
        lead = float(row.get("Lead Time", 0) or 0)
        expected = float(row.get("Expected Lead", 7) or 7)
        margin = float(row.get("Profit Margin", 0) or 0)
        delay_pressure = min(65, max(0, (lead - expected) * 9))
        mode_pressure = {"Same Day": 18, "First Class": 12, "Second Class": 8, "Standard Class": 5}.get(row.get("Ship Mode"), 6)
        margin_pressure = 15 if margin < 0.15 else 8 if margin < 0.3 else 2
        return int(min(100, delay_pressure + mode_pressure + margin_pressure + 12))

    def add_predictions(self) -> pd.DataFrame:
        """Vectorized scoring for fast page loads."""
        df = self.df.copy()
        lead = df["Lead Time"].fillna(0).astype(float)
        expected = df["Expected Lead"].fillna(7).astype(float)
        margin = df["Profit Margin"].fillna(0).astype(float)
        delay_pressure = ((lead - expected).clip(lower=0) * 9).clip(upper=65)
        mode_pressure = df["Ship Mode"].map({"Same Day": 18, "First Class": 12, "Second Class": 8, "Standard Class": 5}).fillna(6)
        margin_pressure = np.select([margin < 0.15, margin < 0.30], [15, 8], default=2)
        df["AI Risk Score"] = (delay_pressure + mode_pressure + margin_pressure + 12).clip(0, 100).round().astype(int)
        df["AI Risk Level"] = pd.cut(df["AI Risk Score"], bins=[-1,35,65,100], labels=["Low", "Medium", "High"])
        df["AI Recommendation"] = np.select(
            [df["AI Risk Score"] >= 75, df["AI Risk Score"] >= 50, df["AI Risk Score"] < 50],
            ["Escalate shipment and review route immediately", "Monitor SLA and optimize carrier priority", "Normal flow - continue tracking"],
            default="Review shipment"
        )
        return df

    def kpi_summary(self) -> dict:
        df = self.add_predictions()
        return {
            "shipments": int(len(df)),
            "high_risk": int((df["AI Risk Level"] == "High").sum()),
            "avg_risk": round(float(df["AI Risk Score"].mean()), 1),
            "delay_rate": round(float(df["Delayed"].mean() * 100), 1),
            "profit": round(float(df.get("Gross Profit", pd.Series(dtype=float)).sum()), 2),
            "avg_lead": round(float(df["Lead Time"].mean()), 1),
        }

    def bottlenecks(self, by="State/Province", top_n=10) -> pd.DataFrame:
        df = self.add_predictions()
        out = df.groupby(by, observed=True).agg(
            Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Delay_Rate=("Delayed", "mean"),
            Avg_AI_Risk=("AI Risk Score", "mean"),
            Gross_Profit=("Gross Profit", "sum"),
        ).reset_index()
        out["Delay_Rate"] = (out["Delay_Rate"] * 100).round(1)
        return out.sort_values(["Avg_AI_Risk", "Delay_Rate", "Shipments"], ascending=False).head(top_n)

    def recommendations(self):
        k = self.kpi_summary()
        recs = []
        if k["delay_rate"] > 50:
            recs.append("Delay rate is critical. Prioritize Same Day and First Class SLA lanes for immediate review.")
        if k["avg_risk"] > 55:
            recs.append("Average AI risk is elevated. Create an operations watchlist for high-risk states and routes.")
        recs.append("Use the bottleneck table to assign executive attention to the highest risk states first.")
        recs.append("Export high-risk shipments daily for dispatch review and route correction.")
        return recs
