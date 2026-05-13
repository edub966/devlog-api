import sqlite3
from datetime import datetime, timezone

DB_NAME = "devlog.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            project TEXT NOT NULL,
            session_type TEXT NOT NULL,
            duration_mins INTEGER NOT NULL,
            energy_level INTEGER NOT NULL,
            mood TEXT NOT NULL,
            shipped TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def create_session(data):
    conn = get_connection()
    cursor = conn.execute('''
        INSERT INTO sessions(project, session_type, duration_mins, energy_level, mood, shipped, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''',
(
        data["project"],
        data["session_type"],
        data["duration_mins"],
        data["energy_level"],
        data["mood"],
        data["shipped"],
        data.get("notes"),
        datetime.now(timezone.utc).isoformat()
    ))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_sessions(filters=None):
    conn = get_connection()

    query = "SELECT * FROM sessions"
    params = []

    if filters:
        conditions = []

        if "project" in filters:
            conditions.append("project = ?")
            params.append(filters["project"])

        if "session_type" in filters:
            conditions.append("session_type = ?")
            params.append(filters["session_type"])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    rows = conn.execute(query, params).fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result

def get_session_by_id(session_id):
    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM sessions WHERE id = ?",
        (session_id,)
    ).fetchone()

    result = dict(row) if row else None
    conn.close()
    return result


def update_session(session_id, data):
    conn = get_connection()

    allowed_fields = ["project", "session_type", "duration_mins", "energy_level", "mood", "shipped" "notes"]

    fields = [f'[{key}]' for key in data if key in allowed_fields]
    values = [data[key] for key in data if key in allowed_fields]

    if not fields:
        conn.close()
        return False

    values.append(session_id)

    conn.execute(
        f"UPDATE sessions SET {', '.join(fields)} WHERE id = ?",
        values
    )

    conn.commit()
    affected = conn.total_changes
    conn.close()
    return affected > 0


def delete_session(session_id):
    conn = get_connection()
    conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()

    affected = conn.total_changes
    conn.close()
    return affected > 0



