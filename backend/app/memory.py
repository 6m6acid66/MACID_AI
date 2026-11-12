import sqlite3
from pathlib import Path
from datetime import datetime, timezone

from .config import DATABASE_PATH


def get_connection():
    Path(DATABASE_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_memory():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_message(session_id, role, content):
    timestamp = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO conversations
            (session_id, role, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (session_id, role, content, timestamp)
        )


def get_history(session_id, limit=20):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT role, content
            FROM conversations
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit)
        ).fetchall()

    return [
        {"role": row["role"], "content": row["content"]}
        for row in reversed(rows)
    ]
