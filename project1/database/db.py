
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "nassau_enterprise.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database(df: pd.DataFrame):
    """Create DB tables once. Avoid rewriting the full CSV on every page rerun."""
    with get_connection() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS ai_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            message TEXT
        )
        """)
        existing = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shipments'").fetchone()
        if existing is None:
            df.to_sql("shipments", con, if_exists="replace", index=False)
            con.execute("INSERT INTO ai_activity(event_type, message) VALUES (?, ?)", ("BOOT", "Enterprise AI logistics engine initialized"))


def log_activity(event_type: str, message: str):
    with get_connection() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS ai_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            message TEXT
        )
        """)
        con.execute("INSERT INTO ai_activity(event_type, message) VALUES (?, ?)", (event_type, message))


def read_activity(limit=20):
    with get_connection() as con:
        return pd.read_sql_query("SELECT * FROM ai_activity ORDER BY id DESC LIMIT ?", con, params=(limit,))
