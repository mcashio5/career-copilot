import os
import sqlite3
from datetime import datetime, timezone

from models import AnalysisResult

# Overridable so the file can live on a mounted volume in production
# (a plain container filesystem is wiped on every redeploy).
DB_PATH = os.environ.get("DB_PATH", "data/history.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                job_title TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                top_matching_skill TEXT NOT NULL,
                top_missing_skill TEXT NOT NULL
            )
            """
        )


def save_analysis(result: AnalysisResult) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO history
                (created_at, job_title, match_score,
                 top_matching_skill, top_missing_skill)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                result.job_title,
                result.match_score,
                result.top_matching_skill,
                result.top_missing_skill,
            ),
        )


def get_history() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM history ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]
